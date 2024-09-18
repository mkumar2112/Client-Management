from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import ClientInfo
from .serializer import ClientInfoserializer
from .Forms import ClientForm
from bson import ObjectId
from decimal import Decimal
from bson.decimal128 import Decimal128

def save_as_pdf(request, id):
    client_info = get_object_or_404(ClientInfo, _id=ObjectId(id))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=client_info_{id}.pdf'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    margin = 100
    line_height = 20
    current_y = height - margin

    def draw_text(text):
        nonlocal current_y
        p.drawString(margin, current_y, text)
        current_y -= line_height

    draw_text(f"Client Name: {client_info.name}")
    draw_text(f"Contact Info: {client_info.phoneNo}")
    draw_text(f"Receive Date: {client_info.receiveDate}")
    draw_text(f"Inventory Received: {client_info.productName}")
    draw_text(f"Reported Issue: {client_info.reportedIssue}")
    draw_text(f"Client Notes: {client_info.clientNotes}")
    draw_text(f"Assigned Technician: {client_info.assignedTechnician}")
    draw_text(f"Estimated Amount: {client_info.estimatedAmount}")
    draw_text(f"Deadline: {client_info.deadline}")
    draw_text(f"Status: {client_info.status}")

    

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def objectToList(clientinfo):
    client_data_list = [{'id': str(client._id), 'name': client.name, 'phoneNo': client.phoneNo,
                         'receiveDate': client.receiveDate, 'productName': client.productName,
                         'reportedIssue': client.reportedIssue, 'clientNotes': client.clientNotes,
                         'assignedTechnician': client.assignedTechnician, 'estimatedAmount': client.estimatedAmount,
                         'deadline': client.deadline, 'status': client.status}
                        for client in clientinfo]
    return client_data_list

def client_list(request):
    search_name = request.GET.get('search', None)
    if search_name:
        clients = ClientInfo.objects.filter(name__icontains=search_name)
    else:
        clients = ClientInfo.objects.all()

    client_data_list = objectToList(clients)
    return render(request, 'home.html', {'status': 200, 'message': 'Client data', 'data': client_data_list})

def client_detail(request, id):
    try:
        client = ClientInfo.objects.get(_id=ObjectId(id))

        if request.method == 'POST':
            note = request.POST.get('note')
            if note is not None:
                if isinstance(client.estimatedAmount, Decimal128):
                    client.estimatedAmount = Decimal(str(client.estimatedAmount))
                else:
                    client.estimatedAmount = Decimal(client.estimatedAmount)

                client.clientNotes = note
                client.save()
                return redirect('client-detail', id=id)

        serialized_client = ClientInfoserializer(client)
        return render(request, 'view.html', {
            'status': 200,
            'message': 'Client found',
            'data': serialized_client.data,
            'id': id
        })

    except ClientInfo.DoesNotExist:
        return render(request, 'error.html', {'status': 404, 'error': 'Client not found'})
    except Exception as e:
        return render(request, 'error.html', {'status': 500, 'error': 'Server error'})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client-list')
    else:
        form = ClientForm()
    return render(request, 'NewJob.html', {'form': form})

def update_client(request, id):
    client = get_object_or_404(ClientInfo, _id=ObjectId(id))

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-list')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'Edit.html', {'form': form, 'client': client})

def delete_client(request, id):
    client = get_object_or_404(ClientInfo, _id=ObjectId(id))
    
    if request.method == 'POST':
        client.delete()
        return redirect('client-list')
    
    return render(request, 'home.html', {'client': client})
