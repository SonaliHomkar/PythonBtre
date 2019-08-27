from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactN
from django.core.mail import send_mail

def contact(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        #realtor_email = request.POST['realtor_email']

        # if user has already submitted inquiry

        if request.user.is_authenticated:
                user_id = request.user.id
                has_contacted = ContactN.objects.all().filter(listing_id = listing_id, user_id = user_id )
                print('into is authenticated')
                if has_contacted:
                        print('into has contacted')
                        messages.error(request, 'You have already made an enquiry for this listing')
                        return redirect('/listing/' + listing_id)
                
        contact = ContactN(listing = listing, listing_id=listing_id, name=name,
        email=email, phone=phone, message=message, user_id = user_id)

        contact.save()

        # send email
        send_mail('Property listing inquiry',
        'There has been inquiry list ' + listing + '. Sign into admin panel for more details',
        'sonali.hirve@gmail.com',
        ['ahomkar@gmail.com','sonali.hirve@gmail.com'],
        fail_silently=False        
        )
        print('sent mail')


        messages.success(request, 'Your request has been submitted successfully')
        return redirect('/listing/' + listing_id)


