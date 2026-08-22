from datetime import date

from .models import EmployeeContract, ContractNotification
from .services.telegram import send_telegram_message


def check_contract_expiration():

    today = date.today()

    contracts = EmployeeContract.objects.select_related(
        'user'
    ).filter(
        status='ACTIVE'
    )

    reminder_days = [30, 14, 7, 3, 1]

    for contract in contracts:

        remaining_days = (
            contract.end_date - today
        ).days

        # Kontrak sudah berakhir
        if remaining_days < 0:

            if contract.status != 'EXPIRED':

                contract.status = 'EXPIRED'

                contract.save(
                    update_fields=['status']
                )

            continue

        # Tentukan reminder yang harus dikirim
        reminder_day = None

        for day in reminder_days:

            if remaining_days <= day:

                reminder_day = day
                break

        if reminder_day is None:
            continue

        # Cek apakah reminder sudah pernah dikirim
        already_sent = ContractNotification.objects.filter(
            contract=contract,
            notification_type='EMPLOYEE',
            days_remaining=reminder_day
        ).exists()

        if already_sent:
            continue

        send_contract_notification(
            contract,
            remaining_days
        )

        ContractNotification.objects.create(
            contract=contract,
            notification_type='EMPLOYEE',
            days_remaining=reminder_day
        )


def send_contract_notification(
    contract,
    remaining_days
):

    user = contract.user

    message = (
        "⚠️ PENGINGAT MASA KONTRAK\n\n"
        f"Nama: {user.name}\n"
        f"NIK: {user.nik}\n"
        f"No. Kontrak: {contract.contract_number}\n"
        f"Berakhir: "
        f"{contract.end_date.strftime('%d-%m-%Y')}\n"
        f"Sisa: {remaining_days} hari"
    )

    if user.telegram_chat_id:

        send_telegram_message(
            user.telegram_chat_id,
            message
        )