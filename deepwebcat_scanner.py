from colorama import Fore
import subprocess
import time
import folium
import random

Y = Fore.LIGHTYELLOW_EX
R = Fore.LIGHTRED_EX
N = Fore.RESET

def get_color(rssi):
    if rssi > -50:
        return 'green'
    elif rssi > -70:
        return 'orange'
    else:
        return 'red'
    
def parse_scan_results(raw_output):
    networks = []
    lines = raw_output.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line or 'BSSID' in line or '----' in line:
            continue
        
        parts = line.split()
        
        if len(parts) < 6:
            continue
        
        try:
            bssid = parts[0]
            frequency = parts[1]
            rssi = int(parts[2])
            
            flags_start = None
            for i in range(4, len(parts)):
                if parts[i].startswith('['):
                    flags_start = i
                    break
            
            if flags_start is None:
                ssid = ' '.join(parts[4:])
                flags = ''
            else:
                ssid_parts = parts[4:flags_start]
                ssid = ' '.join(ssid_parts) if ssid_parts else '<hidden>'
                flags = ' '.join(parts[flags_start:])
            
            networks.append({
                'bssid': bssid,
                'frequency': frequency,
                'rssi': rssi,
                'ssid': ssid,
                'security': flags if flags else 'Unknown'
            })
            
        except (ValueError, IndexError):
            continue
    
    return networks

def detect_evil_twin(networks):
    ssid_groups = {}
    for net in networks:
        ssid = net['ssid']
        if ssid not in ssid_groups:
            ssid_groups[ssid] = []
        ssid_groups[ssid].append(net)
    
    evil_twins = []
    for ssid, nets in ssid_groups.items():
        if ssid == '<hidden>' or not ssid:
            continue
        
        bssids = set()
        for net in nets:
            bssids.add(net['bssid'].lower())
        
        if len(bssids) > 1:
            evil_twins.append({
                'ssid': ssid,
                'networks': nets,
                'bssids': bssids
            })
    
    return evil_twins

ADB_PATH = r'C:\Users\Лук\Desktop\platform-tools\adb.exe' # <- Если у тебя другой путь, замени на свой.

print('---------------------------------------------------------------------------------------\n')

print('██████╗ ███████╗███████╗██████╗ ██╗    ██╗███████╗██████╗      ██████╗ █████╗ ████████╗')
print('██╔══██╗██╔════╝██╔════╝██╔══██╗██║    ██║██╔════╝██╔══██╗    ██╔════╝██╔══██╗╚══██╔══╝')
print('██║  ██║█████╗  █████╗  ██████╔╝██║ █╗ ██║█████╗  ██████╔╝    ██║     ███████║   ██║   ')
print('██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ██║███╗██║██╔══╝  ██╔══██╗    ██║     ██╔══██║   ██║   ')
print('██████╔╝███████╗███████╗██║     ╚███╔███╔╝███████╗██████╔╝    ╚██████╗██║  ██║   ██║   ')
print('╚═════╝ ╚══════╝╚══════╝╚═╝      ╚══╝╚══╝ ╚══════╝╚═════╝      ╚═════╝╚═╝  ╚═╝   ╚═╝ \n')

print('---------------------------------------------------------------------------------------\n')

print('Кодер : SuperDeepWebCat                         Версия утилиты : 1.0\n')

print('Утилита предназначена для управления Wi-Fi через ПК, при этом не имея Wi-Fi адаптера.\n')

print('Инструкция по подключению\n')

print(f'1. {Y}Для включения, перейдите в Настройки -> Для разработчиков -> Беспроводная отладка{N}')
print(f'2. {Y}Включите беспроводную отладку, и запомните 6-значный код{N}')
print(f'3. {Y}Введите 6-значный код который показал ваш телефон, мы будем отслеживать Wi-Fi с телефона{N}\n')

print('Предупреждения по использованию\n')

print(f'1. {R}У вас должен быть телефон Android 11 и выше!{N}')
print(f'2. {R}Удостоверьтесь что в разделе "ПОДКЛЮЧЕННЫЕ УСТРОЙСТВА" появилось устройство!{N}')
print(f'3. {R}Ваша ОС должна быть именно Windows, команды в CLI рассчитаны под эту ОС!{N}')
print(f'4. {R}У вас должен быть установлен ADB, ниже я дал ссылку на оффициальный сайт ADB!{N}')
print(f'5. {R}У вас должен быть включен режим разработчика!{N}\n')

print('---------------------------------------------------------------------------------------\n')

print('Почитай о ADB с официального сайта : https://developer.android.com/tools/releases/platform-tools')
print('Качай ADB для Windows (64-bit) : https://dl.google.com/android/repository/platform-tools-latest-windows.zip\n')

print('Распакуй ZIP на рабочий стол -> Зайди в папку platform-tools -> Открой файл adb.exe')
print(r'Если хочешь проверить работу ADB, открой CLI и введи : "C:\Users\ПОЛЬЗОВАТЕЛЬ\Desktop\platform-tools\adb.exe" --version\n')

print('Если вы сделали все правильно, вам покажет что-то по типу : Android Debug Bri.. и т.д\n')

print('---------------------------------------------------------------------------------------\n')

def run_wifi(command):
    try:
        full_command = f'"{ADB_PATH}" {command}'
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            shell=True,
            timeout=10
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return('[!] Команда зависла и была прервана.')
    except FileNotFoundError:
        return(f'[!] ADB не найден по пути: {ADB_PATH}')
    except Exception as e:
        return f'[!] Ошибка выполнения : {e}.'
    
super_wifi = input('Сколько телефонов вы хотите подключить? (назовите число) : ')

while not super_wifi.isdigit():
    print(f'{R}Введите ЧИСЛО!{N}')
    super_wifi = input('Сколько телефонов вы хотите подключить? (назовите число) : ')

count = int(super_wifi)

phones = []

for i in range(count):
    print(f'\n--- Телефон {i+1} из {count} ---')
    ip = input('Введите IP телефона (например 192.168.1.5) : ')
    pair_port = input('Введите порт сопряжения (например 37921) : ')
    code = input('Введите 6-значный код для сопряжения (например 000000) : ')
    
    phone = {
        'ip': ip,
        'pair_port': pair_port,
        'code': code
    }
    phones.append(phone)
    
    proc = subprocess.Popen(
        f'"{ADB_PATH}" pair {ip}:{pair_port}',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )
    stdout, stderr = proc.communicate(input=f'{code}\n')
    print(stdout + stderr)

print('\nВсе телефоны сопряжены!')

# информация о отображенных устройствах

for i, phone in enumerate(phones):
    print(f'\n--- Подключение телефона {i+1} ({phone["ip"]}) ---')
    connect_port = input('Введите порт подключения (с экрана телефона) : ')
    
    connect_result = run_wifi(f'connect {phone["ip"]}:{connect_port}')
    print(connect_result)
    
    print(f'Сканируем Wi-Fi сети с телефона {i+1}...')
    run_wifi('shell cmd wifi start-scan')
    time.sleep(3)
    
    print(f'\nНайденные сети (телефон {i+1}):')
    print(run_wifi('shell cmd wifi list-scan-results'))

print('\nВсе подключённые устройства:')
print(run_wifi('devices'))

# строим карту с реальными данными

raw_output = run_wifi('shell cmd wifi list-scan-results')
print('\nПарсим результаты сканирования...')

networks = parse_scan_results(raw_output)

print(f'\n===== НАЙДЕНО {len(networks)} СЕТЕЙ =====')
for i, net in enumerate(networks):
    print(f'{i+1}. {net["ssid"]} | RSSI: {net["rssi"]} | Цвет: {get_color(net["rssi"])}')
print('=================================\n')

evil_twins = detect_evil_twin(networks)

if evil_twins:
    print(f'{R}[!] ОБНАРУЖЕН ПОДОЗРИТЕЛЬНЫЙ ДВОЙНИК!{N}')
    
    for twin in evil_twins:
        print(f'\n{Y}[!] Сеть: {twin["ssid"]}{N}')
        print(f'    Найдено {len(twin["bssids"])} разных MAC-адресов:')
        for net in twin['networks']:
            print(f'    • BSSID: {net["bssid"]} | RSSI: {net["rssi"]} dBm | Частота: {net["frequency"]} MHz')
        print(f'    {R}[?] Внимание! Возможна атака "Злой двойник"!{N}')
else:
    print(f'\n{Y}[✓] Подозрительных сетей не обнаружено.{N}')

# карта
if networks:
    print(f'\nНайдено {len(networks)} сетей для карты')
    
    print('\n--- Координаты для карты ---')
    print('Узнать координаты: открой Google Карты, нажми правой кнопкой по месту, выбери "Что здесь?"')
    lat = float(input('Введите широту (например 48.707205): '))
    lon = float(input('Введите долготу (например 44.517036): '))
    
    html_map = folium.Map(location=[lat, lon], zoom_start=15)
    
    for net in networks:
        color = get_color(net['rssi'])
        lat_offset = random.uniform(-0.0003, 0.0003)
        lon_offset = random.uniform(-0.0003, 0.0003)
        
        folium.Marker(
            location=[lat + lat_offset, lon + lon_offset],
            popup=f"<b>{net['ssid']}</b><br>RSSI: {net['rssi']} dBm<br>BSSID: {net['bssid']}",
            icon=folium.Icon(color=color, icon='wifi', prefix='fa')
        ).add_to(html_map)
    
    html_map.save('wifi_map.html')
    print(f'\n[✓] Карта сохранена в wifi_map.html ({len(networks)} сетей)')
    print('Открой этот файл в браузере чтобы увидеть карту!')
else:
    print('[!] Сети не найдены или ошибка парсинга')

input('\nНажмите Enter для выхода...')
