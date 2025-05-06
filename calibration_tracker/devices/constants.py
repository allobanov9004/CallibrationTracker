#models const
STATUS_CHOICES = (
    ('valid', 'Актуально'),
    ('overdue', 'Просрочено'),
    ('storage', 'Хранение'),
)

STATUS = [
    ('valid', 'Действующий'),
    ('overdue', 'Просрочен'),
    ('storage', 'Хранение'),
    ('calibration', 'В поверке'),
    ('calibration_done', 'Поверено'),
    ('rejected', 'Не пригодно к применению'),
]

MEASURE_TYPE = [
    ('pressure', 'Давление'),
    ('thermal', 'Теплотехнические величины'),
    ('electrical', 'Электрические величины'),
    ('linear_and_angular_dimensions', 'Линейные и угловые размеры'),
    ('mechanical', 'Механические величины'),
    ('flow', 'Расход'),
    ('other', 'Другое'),
]

STATUS_DISPLAY = {
            'valid': 'Актуально',
            'overdue': 'Просрочено',
            'storage': 'Хранение',
            'calibration': 'В поверке',
            'rejected': 'Забраковано'
}

STATUS_LABEL_CLASS = {
            'valid': 'bg-success',
            'overdue': 'bg-danger',
            'storage': 'bg-secondary',
            'calibration': 'bg-info',
            'rejected': 'bg-dark'
}

#forms

UNIT_CHOICES = {
    'electrical': ['В', 'А', 'Ом', 'Вт', 'Гц'],
    'pressure': ['кПа', 'бар', 'МПа', 'кгс/см²', 'атм'],
    'thermal': ['°C', 'K'],
    'linear_and_angular_dimensions': ['мм', 'см', 'м', '°'],
    'mechanical': ['Н', 'кН', 'кг', 'г'],
    'flow': ['м³/ч', 'л/мин', 'м³/с'],
    'other': ['—']
}