# Система контроля посещаемости занятий в учебных заведениях
## Индивидуальный проект Samsung IoT академии

Учёт посещаемости студентов и преподавателей, составление отчета по каждому учащемуся и преподавателю.  
Студент или преподавать должны приложить свою карту к считывателю при входе в аудиторию, тем самым учтётся его присудствие.  

Структура репозитория:  
- webapp  
    Содержит django сервер, логику проекта  
- emulator  
    Вспомогательные скрипты для отладки и тестирования веб-приложения  
- nfc_script  
    Скрипт для работы со считывателем nfc карт