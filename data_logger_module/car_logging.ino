#include <SD.h>
#include <SPI.h>

File car;
char *arr = new char[64], *arr2 = new char[64];
bool one = false, two = false;
int i;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);

  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");
  clean(arr, 64);
  clean(arr2, 64);
}

void clean(char *arr, int n)
{
  for (int j = 0; j < n; j++)
    arr[j] = '\0';
}

void loop() {
  //0 kouts 1 corey
  if (Serial1.available()) {
    i = 0;
    while (Serial1.available()) {
      arr[i] = Serial1.read();
      if (arr[i] == '\n') {
        break;
      }
      i++;
      delay(1);
    }
    Serial.write('0');
    Serial.write(';');
    Serial.write(arr);
    Serial.write('\n');
    car = SD.open("car.txt", FILE_WRITE);
    car.write(arr);
    car.close();
  }

  if (Serial2.available()) {
    i = 0;
    while (Serial2.available()) {
      arr2[i] = Serial2.read();
      if (arr2[i] == '\n') {
        break;
      }
      i++;
      delay(1);
    }
    Serial.write('1');
    Serial.write(';');
    Serial.write(arr2);
    Serial.write('\n');
    car = SD.open("car.txt", FILE_WRITE);
    car.write(arr2);
    car.close();
  }
  clean(arr, 64);
  clean(arr2, 64);
  delay(150);
}






