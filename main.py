import csv
import sys
from os import system, name

HABITATS = {
  1: 'Perairan pantai',
  2: 'Paparan benua',
  3: 'Oseanik',
  4: 'Laut dalam',
  5: 'Perairan karang'
}

def error(message):
  clear_terminal()
  print(message)
  input('\n<tekan Enter untuk keluar>')
  sys.exit(f"An error occured: {message}")

def clear_terminal():
  if name == 'nt':
      _ = system('cls')
  else:
      _ = system('clear')

  print("Identifikasi Hiu")
  print("oleh 13518052 dan 13518148\n")

def get_question(candidates, asked):
  for shark in candidates:
    if shark['pertanyaan_1'] != '' and abs(int(shark['pertanyaan_1'])) not in asked: return abs(int(shark['pertanyaan_1']))
    if shark['pertanyaan_2'] != '' and abs(int(shark['pertanyaan_2'])) not in asked: return abs(int(shark['pertanyaan_2']))
    if shark['pertanyaan_3'] != '' and abs(int(shark['pertanyaan_3'])) not in asked: return abs(int(shark['pertanyaan_3']))
  return None

def print_shark(shark):
  print(f"Nama         : Hiu {shark['nama']}")
  print(f"Nomenclature : {shark['genus']} {shark['spesies']}")
  print(f"Keberadaan   : {shark['keberadaan']}")
  print(f"Habitat      : {shark['habitat']}")
  if (shark['min_ukuran'] != '-'):
    print(f"Ukuran       : {shark['min_ukuran']} - {shark['max_ukuran']}cm")

def check_all_answered(candidates, answers):
  for i in range(len(candidates)):
    shark = candidates[i]
    if (shark['pertanyaan_1'] == '' or int(shark['pertanyaan_1']) in answers) and (shark['pertanyaan_2'] == '' or int(shark['pertanyaan_2']) in answers) and (shark['pertanyaan_3'] == '' or int(shark['pertanyaan_3']) in answers):
      return i
  return None

def main():
  clear_terminal()

  print("Memuat data hiu...")
  sharks = []
  with open('main.csv', newline='') as main_csv:
    reader = csv.reader(main_csv, delimiter=',')
    header = []
    i = 0
    for row in reader:
      if i == 0:
        header = row
      else:
        shark = {}
        for j in range(len(header)):
          shark[header[j]] = row[j]
        sharks.append(shark)
      i += 1

  print("Memuat data pertanyaan...")
  questions = []
  with open('questions.csv', newline='') as main_csv:
    reader = csv.reader(main_csv, delimiter=',')
    header_read = False
    for row in reader:
      if header_read:
        questions.append(row[0])
      else:
        header_read = True

  clear_terminal()
  print("Pertanyaan Habitat:")
  print("Dimana tempat Anda menemukan hiu ini?\n")
  print("Pilihan:")
  print("[1] Perairan pantai, payau, atau sungai")
  print("[2] Paparan benua")
  print("[3] Oseanik")
  print("[4] Laut dalam")
  print("[5] Perairan karang\n")
  print("Pilih nomor yang paling sesuai!")
  habitat_str = input("Jawaban: ")
  habitat = HABITATS[int(habitat_str)] if habitat_str.isdecimal() else None
  if habitat is None:
    error("Pilih nomor yang valid!")

  clear_terminal()
  print("Pertanyaan Ukuran:")
  print("Berapa ukuran atau panjang hiu tersebut dalam satuan centimeter?\n")
  length_str = input("Jawaban: ")
  length = int(length_str) if length_str.isdecimal() else None
  if length is None or length < 1:
    error("Masukan ukuran yang valid!")

  candidates = list(filter(lambda shark: shark['habitat'] == habitat and (shark['min_ukuran'] == '-' or (length > int(shark['min_ukuran']) and length < int(shark['max_ukuran']))), sharks))
  answers = set()
  asked = set()
  result = -1

  clear_terminal()
  print("Pertanyaan Ciri-Ciri:\n")

  while len(candidates) > 0 and result < 0:
    candidate_question = get_question(candidates, asked)
    print(questions[candidate_question])
    asked.add(candidate_question)
    answer = input('Jawaban (y/n): ')
    if answer == 'y':
      answers.add(candidate_question)
    else:
      answers.add(-candidate_question)
    candidates = list(filter(lambda shark: (shark['pertanyaan_1'] == '' or -int(shark['pertanyaan_1']) not in answers) and (shark['pertanyaan_2'] == '' or -int(shark['pertanyaan_2']) not in answers) and (shark['pertanyaan_3'] == '' or -int(shark['pertanyaan_3']) not in answers),  candidates))
    complete = check_all_answered(candidates, answers)
    if complete is not None:
      result = complete

  clear_terminal()
  if result == -1:
    print("Tidak ada hiu yang sesuai dengan kriteria Anda!")
  else:
    print("Hiu berikut memenuhi kriteria pencarian Anda:\n")
    print_shark(candidates[result])
  input("\n<tekan Enter untuk keluar>")
  
if __name__ == "__main__":
  main()