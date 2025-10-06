import requests, os
from mailjet_rest import Client

def send_email(to_address: str, from_adress: str, from_name: str, subject: str, message: str):
    
    MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
    MAILJET_SECRET_KEY = os.environ['MAILJET_SECRET_KEY']

    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')
    data = {
        'Messages': [
            {
                'From': {
                    'Email': from_adress,
                    'Name': from_name
                },
                'To': [
                    {
                        'Email': to_address,
                    },
                    {
                        'Email': 'conecopiagelato@gmail.com',
                        'Name': 'Tony DeSante from Conecopia LLC'
                    }
                ],
                'Subject': subject,
                'HTMLPart': message
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(f'Email Status: {result.status_code}, Body: {result.json()}')

def generate_email(items: list, total: str, message: str):
    items_html = list(
        map(
            lambda item: f'''
                <tr>
                    <td align="right">{ item['product'].name }</td>
                    <td align="center">{ item['quantity'] }</td>
                    <td align="left">{ item['total_price'] / 100 }</td>
                </tr>
            ''', 
            items
        )
    )

    template = f'''
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; margin: 0;">
            <tr>
                <td>
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; overflow: hidden;">
                        <tr>
                        <td style="background-color: #f2b705; color: #333; text-align: center; padding: 20px 10px;">
                            <h1 style="margin: 0; font-size: 24px;">Thank you for your order!</h1>
                            <p style="margin: 5px 0 0; font-size: 16px;">Conecopia Gelato LLC</p>
                        </td>
                        </tr>
                        <tr>
                            <td style="padding: 20px;">
                                <p style="font-size: 15px; color: #555;">Here\'s a summary of your recent order:</p>
                                <table width="100%" cellpadding="6" cellspacing="0" border="0" style="border-collapse: collapse;">
                                    <tr style="background-color: #f7f7f7; border-bottom: 1px solid #ddd;">
                                        <th align="left">Item</th>
                                        <th align="center">Qty</th>
                                        <th align="right">Price</th>
                                    </tr>
                                    { "".join(items_html) }
                                    <tr>
                                        <td colspan="2" align="right" style="font-weight: bold; border-top: 1px solid #ddd;">Total:</td>
                                        <td align="right" style="font-weight: bold; border-top: 1px solid #ddd;">${ total / 100 }</td>
                                    </tr>
                                </table>

                                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

                                <blockquote style="margin: 10px 0; padding: 10px 15px; background-color: #fff8e1; border-left: 4px solid #f2b705; font-style: italic; color: #444;">
                                { message }
                                </blockquote>

                                <p style="font-size: 14px; color: #888; text-align: center; margin-top: 40px;">
                                    Conecopia Gelato LLC<br>
                                    <a href="https://www.conecopia.com" style="color: #f2b705; text-decoration: none;">www.conecopia.com</a>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    '''

    return template