from django.utils import timezone

from app.models import Users, EmployeeContract, ContractNotification
from .telegram import send_telegram_message


REMINDER_DAYS = [30, 14, 7, 3, 1]


def check_employee_contract(user):

    now = timezone.localtime(timezone.now())
    today = now.date()

    contract = (
        EmployeeContract.objects
        .filter(
            user=user,
            status='ACTIVE',
            start_date__lte=today,
            end_date__gte=today
        )
        .order_by('-end_date')
        .first()
    )

    if not contract:
        return

    remaining_days = (
        contract.end_date - today
    ).days

    if remaining_days <= 1:
        if contract.status != 'EXPIRED':
            contract.status = 'EXPIRED'
            contract.save(
                update_fields=['status']
            )

    print(
        f"Contract {contract.contract_number} "
        f"for user {user} "
        f"has {remaining_days} days remaining."
    )

    eligible_reminders = [
        day
        for day in REMINDER_DAYS
        if remaining_days <= day
    ]

    if not eligible_reminders:
        return

    for reminder_day in sorted(eligible_reminders, reverse=True):

        employee_sent = ContractNotification.objects.filter(
            contract=contract,
            notification_type='EMPLOYEE',
            reminder_day=reminder_day
        ).exists()

        hrd_sent = ContractNotification.objects.filter(
            contract=contract,
            notification_type='HRD',
            reminder_day=reminder_day
        ).exists()

        if employee_sent and hrd_sent:
            continue

        send_contract_reminder(
            contract=contract,
            remaining_days=remaining_days,
            reminder_day=reminder_day
        )

        return

def send_contract_reminder(contract, remaining_days, reminder_day):

    user = contract.user

    # ==========================
    # NOTIFIKASI KARYAWAN
    # ==========================
    if user.telegram_chat_id:
        employee_sent = ContractNotification.objects.filter(
            contract=contract,
            notification_type='EMPLOYEE',
            reminder_day=reminder_day 
        ).exists()

        if not employee_sent:
            message = (
                "⚠️ PENGINGAT MASA KONTRAK\n\n"
                f"Halo {user.name},\n\n"
                f"Kontrak Anda akan berakhir dalam {remaining_days} hari.\n\n"
                f"Nomor Kontrak : {contract.contract_number}\n"
                f"Tanggal Berakhir : {contract.end_date.strftime('%d-%m-%Y')}\n\n"
                f"Silakan menghubungi HRD untuk informasi lebih lanjut."
            )
            send_telegram_message(user.telegram_chat_id, message)

            ContractNotification.objects.create(
                contract=contract,
                notification_type='EMPLOYEE',
                reminder_day=reminder_day
            )


    # ==========================
    # NOTIFIKASI HRD
    # ==========================

    hrd_users = Users.objects.filter(
        is_admin__in=[2],
        telegram_chat_id__isnull=False
    ).exclude(
        telegram_chat_id=''
    )

    for hrd in hrd_users:

        hrd_sent = ContractNotification.objects.filter(
            contract=contract,
            notification_type='HRD',
            reminder_day=reminder_day
        ).exists()

        if hrd_sent:
            continue

        message = (
            "📢 PENGINGAT KONTRAK KARYAWAN\n\n"
            f"Nama : {user.name}\n"
            f"NIK : {user.nik}\n"
            f"Divisi : {user.divisi}\n"
            f"No. Kontrak : {contract.contract_number}\n"
            f"Berakhir : "
            f"{contract.end_date.strftime('%d-%m-%Y')}\n"
            f"Sisa : {remaining_days} hari"
        )

        send_telegram_message(
            hrd.telegram_chat_id,
            message
        )

        ContractNotification.objects.create(
            contract=contract,
            notification_type='HRD',
            reminder_day=reminder_day
        )