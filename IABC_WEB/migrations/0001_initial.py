# Generated by Django 4.0.5 on 2022-07-28 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=100, verbose_name='Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Awards_prof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrant_name', models.CharField(max_length=200, verbose_name='Entrant name')),
                ('mobile_num', models.CharField(max_length=200, verbose_name='Mobile number')),
                ('email_add', models.CharField(max_length=50, unique=True, verbose_name='Email')),
                ('entrant_org', models.CharField(max_length=200, verbose_name='Entrant Organization')),
                ('client_org', models.CharField(max_length=200, verbose_name='Client Organization')),
                ('entrant_title', models.CharField(max_length=200, verbose_name='Entrant Title')),
                ('entry_title', models.CharField(max_length=200, verbose_name='Entry title')),
                ('if_member', models.BooleanField(default=False)),
                ('entrant_membershipnum', models.CharField(max_length=200, verbose_name='Entrant Membership No.')),
                ('entered_before', models.BooleanField(default=False)),
                ('year', models.CharField(blank=True, max_length=200, null=True, verbose_name='Year')),
                ('division', models.CharField(max_length=200, verbose_name='Division')),
                ('category', models.CharField(max_length=200, verbose_name='Category')),
                ('entry_form', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('certtype', models.CharField(max_length=200, verbose_name='Certification Type')),
                ('certification_form', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_plan', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample2', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample3', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('remarks', models.CharField(max_length=200, verbose_name='Remarks')),
                ('agency', models.CharField(max_length=200, verbose_name='Agency')),
                ('is_paid', models.BooleanField(default=False)),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='Entry Date')),
                ('file', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('judged', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Awards_student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrant_name', models.CharField(max_length=200, verbose_name='Entrant name')),
                ('mobile_num', models.CharField(max_length=10, verbose_name='Mobile number')),
                ('email_add', models.CharField(max_length=200, unique=True, verbose_name='Email')),
                ('entrant_school', models.CharField(max_length=200, verbose_name='Entrant school')),
                ('entrant_degree', models.CharField(max_length=200, verbose_name='Entrant degree')),
                ('entry_title', models.CharField(max_length=200, verbose_name='Entry title')),
                ('entered_before', models.BooleanField(default=False)),
                ('year', models.CharField(blank=True, max_length=200, null=True, verbose_name='Year')),
                ('division', models.CharField(max_length=200, verbose_name='Division')),
                ('category', models.CharField(max_length=200, verbose_name='Category')),
                ('entry_form', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('certtype', models.CharField(max_length=200, verbose_name='Certification Type')),
                ('certification_form', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_plan', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample2', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('work_sample3', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('remarks', models.CharField(max_length=200, verbose_name='Remarks')),
                ('is_paid', models.BooleanField(default=False)),
                ('entry_date', models.DateTimeField(auto_now_add=True, verbose_name='Entry Date')),
                ('file', models.FileField(blank=True, null=True, upload_to='AwardsSubmissions/')),
                ('judged', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification', models.CharField(max_length=100, verbose_name='Certification')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_A',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_Name', models.CharField(max_length=100, verbose_name='Industry Name')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_B',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_type', models.CharField(max_length=100, verbose_name='Business Type')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_title', models.CharField(max_length=100, verbose_name='Current Title')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_D',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_area', models.CharField(max_length=100, verbose_name='Key Area')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_E',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_no', models.CharField(max_length=100, verbose_name='Employee Number')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_F',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(max_length=100, verbose_name='Experience')),
            ],
        ),
        migrations.CreateModel(
            name='Chart_G',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(max_length=100, verbose_name='About IABC')),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=100, verbose_name='Division')),
            ],
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priceName', models.CharField(max_length=50, verbose_name='Name')),
                ('priceVal', models.CharField(max_length=50, verbose_name='Value')),
            ],
        ),
        migrations.CreateModel(
            name='Winners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryNo', models.CharField(max_length=100, verbose_name='No.')),
                ('entryName', models.CharField(max_length=100, verbose_name='Entry Name')),
                ('entryCat', models.CharField(max_length=100, verbose_name='Category')),
                ('entrantName', models.CharField(max_length=100, verbose_name='Entrant Name')),
                ('entryComp', models.CharField(max_length=100, verbose_name='Company')),
                ('windate', models.DateField(auto_now_add=True, verbose_name='Winner Date')),
            ],
        ),
        migrations.CreateModel(
            name='Winners2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entryNo', models.CharField(max_length=100, verbose_name='No.')),
                ('entryName', models.CharField(max_length=100, verbose_name='Entry Name')),
                ('entryCat', models.CharField(max_length=100, verbose_name='Category')),
                ('entrantName', models.CharField(max_length=100, verbose_name='Entrant Name')),
                ('entryComp', models.CharField(max_length=100, verbose_name='Company')),
                ('windate', models.DateField(auto_now_add=True, verbose_name='Winner Date')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTrackerName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255, verbose_name='Event Name')),
                ('event_date', models.CharField(max_length=255, verbose_name='Event Date')),
                ('event_end', models.DateTimeField(blank=True, max_length=255, null=True, verbose_name='Event End')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign', models.CharField(max_length=255, verbose_name='Assign')),
                ('assignby', models.CharField(max_length=255, verbose_name='Assign By')),
                ('date_input', models.DateTimeField(auto_now_add=True, verbose_name='Input Date')),
                ('date_dur', models.CharField(max_length=255, verbose_name='Date_duration')),
                ('deadline', models.DateField(max_length=255, verbose_name='Deadline')),
                ('act_Task', models.CharField(max_length=255, verbose_name='Activity Task')),
                ('remarks', models.CharField(max_length=255, verbose_name='Remarks')),
                ('status', models.CharField(blank=True, max_length=255, null=True, verbose_name='Status')),
                ('percent', models.CharField(blank=True, max_length=255, null=True, verbose_name='Percent')),
                ('complete_date', models.DateTimeField(blank=True, max_length=255, null=True, verbose_name='Complete Date')),
                ('proj_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.projecttrackername', verbose_name='proj_id')),
            ],
        ),
        migrations.CreateModel(
            name='OnlinePaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Payment Date')),
                ('typeProduct', models.CharField(max_length=50, verbose_name='Product Type')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='Join Date')),
                ('industry_Name', models.CharField(max_length=200, verbose_name='Industry Name')),
                ('business_type', models.CharField(max_length=200, verbose_name='Business Type')),
                ('current_title', models.CharField(max_length=200, verbose_name='Current Title')),
                ('key_area', models.CharField(max_length=200, verbose_name='Key Area')),
                ('employee_no', models.CharField(max_length=200, verbose_name='No of Employees')),
                ('experience', models.CharField(max_length=200, verbose_name='Experience')),
                ('interest', models.CharField(max_length=200, verbose_name='Interest')),
                ('about', models.CharField(max_length=200, verbose_name='About')),
                ('nick_name', models.CharField(max_length=200, verbose_name='NickName')),
                ('designation', models.CharField(max_length=200, verbose_name='Designation')),
                ('company_name', models.CharField(max_length=200, verbose_name='Company Name')),
                ('floor_no', models.CharField(max_length=200, verbose_name='Floor No')),
                ('building_no', models.CharField(max_length=200, verbose_name='Building No')),
                ('street', models.CharField(max_length=200, verbose_name='Street')),
                ('baranggay', models.CharField(max_length=200, verbose_name='Baranggay')),
                ('city', models.CharField(max_length=200, verbose_name='City')),
                ('region', models.CharField(max_length=200, verbose_name='Region')),
                ('postal_zip', models.CharField(max_length=4, verbose_name='Postal Zip')),
                ('telephone_no', models.CharField(max_length=200, verbose_name='Telephone No')),
                ('fax_no', models.CharField(max_length=200, verbose_name='Fax No')),
                ('mobile_no', models.CharField(max_length=200, verbose_name='Mobile No')),
                ('email_address', models.CharField(max_length=200, verbose_name='Email')),
                ('birthday', models.CharField(max_length=200, verbose_name='Birthday')),
                ('membership', models.BooleanField(default=False)),
                ('ceo_excel', models.BooleanField(default=False)),
                ('regional_conf', models.BooleanField(default=False)),
                ('media_relations', models.BooleanField(default=False)),
                ('digital_comm', models.BooleanField(default=False)),
                ('phil_quill', models.BooleanField(default=False)),
                ('publication', models.BooleanField(default=False)),
                ('sponsorship', models.BooleanField(default=False)),
                ('question_1', models.CharField(max_length=4)),
                ('question_2', models.CharField(max_length=4)),
                ('share_contact', models.BooleanField(default=False)),
                ('receive_announce', models.BooleanField(default=False)),
                ('profile_photo', models.FileField(blank=True, null=True, upload_to='MembersSubmissions/')),
                ('expiry_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='Expiry Date')),
                ('is_paid', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='MembersSubmissions/')),
                ('received_email', models.BooleanField(default=False)),
                ('for_renewal', models.BooleanField(default=False)),
                ('renewalfile', models.FileField(blank=True, null=True, upload_to='MembersSubmissions/')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Checkpayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cperson', models.CharField(max_length=50, verbose_name='Contact Person')),
                ('cnum', models.CharField(max_length=50, verbose_name='Contact Number')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('awards_profid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.awards_prof', verbose_name='awards_profid')),
                ('awards_studentid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.awards_student', verbose_name='awards_studentid')),
                ('membership_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.members', unique=True, verbose_name='membership_id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(blank=True, max_length=255, null=True, verbose_name='End Date')),
                ('checks', models.CharField(max_length=255, verbose_name='Checks')),
                ('listcheck', models.BooleanField(default=False)),
                ('proj_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.projecttracker', verbose_name='proj_id')),
            ],
        ),
        migrations.CreateModel(
            name='BidderSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='BidderSubmissions/')),
                ('description', models.CharField(max_length=50, verbose_name='Description')),
                ('comments', models.CharField(max_length=50, verbose_name='Comments')),
                ('status', models.CharField(default='Pending', max_length=50, verbose_name='Status')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.AddField(
            model_name='awards_prof',
            name='membership_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='IABC_WEB.members', verbose_name='membership_id'),
        ),
        migrations.AddField(
            model_name='awards_prof',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id'),
        ),
    ]