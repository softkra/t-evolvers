from django.shortcuts import render
from rest_framework.views import APIView
from .models import Metrics, Notifications
from rest_framework.response import Response
from rest_framework import status
from .serializers import MetricSerializer, NotificationsSerializer
from django.http import Http404
from datetime import date
from django.db.models import Avg, Max
from datetime import datetime, timedelta
import csv
from django.http import HttpResponse, JsonResponse, FileResponse
from uuid import UUID
import io
import xlsxwriter
# Create your views here.

class MetricList(APIView):
    def get(self, request):
        metrics = Metrics.objects.all()
        serializer = MetricSerializer(metrics, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MetricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MetricDetails(APIView):
    def get_queryset(self, pk):
        try:
            return Metrics.objects.get(pk=pk)
        except Metrics.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        metric = self.get_queryset(pk)
        serializer = MetricSerializer(metric)
        return Response(serializer.data)

    def put(self, request, pk):
        metric = self.get_queryset(pk)
        serializer = MetricSerializer(metric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        metric = self.get_queryset(pk)
        metric.delete()
        return Response("Deleted.", status=status.HTTP_204_NO_CONTENT)

class NotificationsApiView(APIView):
    def get(self, request):
        notifications = Notifications.objects.all()
        serializer = NotificationsSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NotificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardApiView(APIView):
    def get(self, request):
        today = date.today()
        notifications = Notifications.objects.filter(created__gte=today).count()
        avg_metric = Metrics.objects.all()
        avg_today = avg_metric.filter(created__gte=today).aggregate(Avg('metric'))
        max_today = avg_metric.filter(created__gte=today).aggregate(Max('metric'))
        avg_month = avg_metric.filter(created__month=today.month).aggregate(Avg('metric'))
        avg_month_by_device = avg_metric.filter(created__month=today.month).values_list('device_id').annotate(Avg('metric'))

        data_response = {
            'notifications': notifications,
            'max_today': max_today['metric__max'],
            'avg_today': avg_today['metric__avg'],
            'avg_month': avg_month['metric__avg'],
            'avg_month_by_device': avg_month_by_device
        }
        return Response(data_response)

def date_range():
    today = date.today()
    start = datetime(today.year, today.month, 1)
    end = datetime(today.year, today.month, today.day)
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days

def CSVReport(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
    )
    try:
        if request.GET:
            sanitize_report_params(request.GET)
    except ValueError as e:
        return JsonResponse({'error':str(e)})

    result = Metrics.objects.all().order_by('-pk')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    device = request.GET.get('device', None)

    if start_date and end_date:
        result = result.filter(report__range=(start_date, end_date))
    if device:
        result = result.filter(device_id=device)

    writer = csv.writer(response)
    writer.writerow(['Dispositivo', 'Metrica', 'Fecha de reporte'])
    for row in result:
        writer.writerow([row.device_id, row.metric, row.report])

    return response

def ExcelReport(request):
    today = date.today()
    notifications = Notifications.objects.filter(created__gte=today).count()
    avg_metric = Metrics.objects.all()
    avg_today = avg_metric.filter(created__gte=today).aggregate(Avg('metric'))
    max_today = avg_metric.filter(created__gte=today).aggregate(Max('metric'))
    avg_month = avg_metric.filter(created__month=today.month).aggregate(Avg('metric'))
    avg_month_by_device = avg_metric.filter(created__month=today.month).values_list('device_id').annotate(Avg('metric'))

    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Promedio de temperatura (mes actual): ')
    worksheet.write('B1', round(avg_month.get('metric__avg', 0)))
    worksheet.write('A2', 'Promedio de temperatura (hoy): ')
    worksheet.write('B2', round(avg_today.get('metric__avg',0)))
    worksheet.write('A3', 'Temperatura maxima reportada (hoy): ')
    worksheet.write('B3', round(max_today.get('metric__max',0)))
    worksheet.write('A4', 'Total notificaciones (hoy): ')
    worksheet.write('B4', notifications)

    worksheet.write('A6', "PROMEDIO POR DISPOSITIVOS", bold)
    worksheet.write('A7', 'Dispositivo:', bold)
    worksheet.write('B7', 'Promedio', bold)

    row = 8
    for val in avg_month_by_device:
        print(val[0])
        worksheet.write(f'A{row}', str(val[0]))
        worksheet.write(f'B{row}', int(round(val[1])))
        row+=1
    
    """           CHART             """
    # Add a chartsheet. A worksheet that only holds a chart.
    chartsheet = workbook.add_chartsheet()

    # Create a new bar chart.
    chart1 = workbook.add_chart({'type': 'bar'})

    # Configure a second series. Note use of alternative syntax to define ranges.
    chart1.add_series({
        'categories': ['Sheet1', 7, 0, (row-1), 0],
        'values':     ['Sheet1', 7, 1, (row-1), 1],
    })

    # Add a chart title and some axis labels.
    chart1.set_title ({'name': 'PROMEDIO POR DISPOSITIVOS'})
    chart1.set_x_axis({'name': 'Temperatura (°C)'})
    chart1.set_y_axis({'name': 'Dispositivos'})

    # Set an Excel chart style.
    chart1.set_style(11)

    # Add the chart to the chartsheet.
    chartsheet.set_chart(chart1)

    # Display the chartsheet as the active sheet when the workbook is opened.
    chartsheet.activate();

    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report.xlsx')

def sanitize_report_params(data):
    start_date = data.get('start_date', None)
    end_date = data.get('end_date', None)
    if '/' in start_date:
        raise ValueError("Invalid date format, suggested format YYYY-MM-DD")
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format, suggested format YYYY-MM-DD")

    device = data.get('device', None)
    try:
        UUID(device, version=4)
    except ValueError:
        raise ValueError("'{}' is not a valid UUID".format(device))

def validate_date(input_date):
    year, month, day = input_date.split('-')

    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False

    if(isValidDate):
        return True
    else:
        return False