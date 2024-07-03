from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contact

class IdentifyView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')
        
        primary_contact = None
        existing_contacts = Contact.objects.filter(email=email) | Contact.objects.filter(phone_number=phone_number)
        
        if existing_contacts.exists():
            primary_contact = existing_contacts.order_by('created_at').first()
            
            if (primary_contact.email and primary_contact.email != email) or (primary_contact.phone_number and primary_contact.phone_number != phone_number):
                new_contact = Contact.objects.create(
                    email=email,
                    phone_number=phone_number,
                    linked_id=primary_contact.id,
                    link_precedence='secondary'
                )
                primary_contact.updated_at = now()
                primary_contact.save()
            else:
                new_contact = primary_contact
        else:
            new_contact = Contact.objects.create(
                email=email,
                phone_number=phone_number,
                link_precedence='primary'
            )
        
        all_linked_contacts = Contact.objects.filter(linked_id=new_contact.id) | Contact.objects.filter(id=new_contact.id)
        emails = list(all_linked_contacts.values_list('email', flat=True))
        phone_numbers = list(all_linked_contacts.values_list('phone_number', flat=True))
        secondary_contact_ids = list(all_linked_contacts.filter(link_precedence='secondary').values_list('id', flat=True))
        
        response_data = {
            "contact": {
                "primaryContactId": primary_contact.id if primary_contact else new_contact.id,
                "emails": emails,
                "phoneNumbers": phone_numbers,
                "secondaryContactIds": secondary_contact_ids
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
