from django.core.management.base import BaseCommand, CommandParser
from notifications.utils import check_calibration_deadlines

class Command(BaseCommand):
    help = 'Проверка сроков поверки средств измерений'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=14,
            help='Количество дней вперед, для которых проверяются сроки поверки(по умолчанию 14)'
        )

    def handle(self, *args, **kwargs) -> None:
        days_ahead = kwargs.get('days_ahead', 14)
        check_calibration_deadlines(days_ahead)
        self.stdout.write(f'Сроки поверки средств измерений проверены на {days_ahead} дней вперед')

