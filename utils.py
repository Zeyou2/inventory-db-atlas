# from datetime import datetime


# def get_date():
#         while True:
#             choose_date = input(f"""
#             A data de entrada foi gerada, ({datetime.strftime(datetime.now(), "%d/%m/%Y")}) confirma essa data como data de entrada?
#             APERTE 'ENTER' SE SIM | ou digite 'N' e aperte ENTER se NÃO """)
#             if choose_date == '':
#                 date = datetime.strftime(datetime.now(), "%y%m%d")
#                 return date
#             elif choose_date.lower() == 'n':
#                 day_in = input("\nDigite o dia desejado: ")
#                 month_in = input("\nDigite o mês desejado: ")
#                 year_in = input("\nDigite o ano desejado: ")
#                 date  = datetime(int(year_in), int(month_in), int(day_in)).strftime("%y%m%d")
#                 return date