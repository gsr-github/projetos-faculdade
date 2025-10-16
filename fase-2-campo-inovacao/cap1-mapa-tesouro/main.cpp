#include <Arduino.h>
#include <math.h>
#include "DHT.h"

// ----------------------------------------------------------------------
  // CONDIÇÕES PARA LIGAR A BOMBA
  // Liga SOMENTE se TODAS forem verdadeiras:
  // 1) NPK_OK      → N, P e K = 1
  // 2) ph_neutro   → 6.9 <= pH <= 7.1
  // 3) humidity_low→ umidade < 40%
  // 4) chuva == false → sem previsão de chuva
  // N P K | pH | Estado(pH) | Umid(%) | NPK_OK | Chuva | Bomba
// ----------------------------------------------------------------------


// =======================
// Pinos
// =======================
#define PIN_DHT    15
#define PIN_LDR    34
#define PIN_RELAY  26
#define PIN_BTN_N  13
#define PIN_BTN_P  12
#define PIN_BTN_K  14

// =======================
// DHT22
// =======================
#define DHTTYPE DHT22
DHT dht(PIN_DHT, DHTTYPE);

// =======================
// Configurações gerais
// =======================
const bool  RELAY_ACTIVE_HIGH   = true;   // troque p/ false se relé for ativo em LOW
const float HUMIDITY_MIN_IRRIGA = 40.0;   // bomba só liga se umidade < 40%
const int   ADC_SAMPLES         = 8;
const unsigned long DEBOUNCE_MS = 30;

// =======================
// Variável chuva (manual via Serial)
// =======================
bool chuva = false; // false = sem chuva (pode irrigar); true = previsão de chuva (bloqueia)

// =======================
// Estados (toggle) dos botões
// =======================
bool stateN = false, stateP = false, stateK = false;
int  lastRawN = HIGH,  lastRawP = HIGH,  lastRawK = HIGH;
unsigned long lastMsN = 0, lastMsP = 0, lastMsK = 0;
bool bombaLigada = false;

// =======================
// Funções auxiliares
// =======================
void setRelay(bool on) {
  digitalWrite(PIN_RELAY, (RELAY_ACTIVE_HIGH ? (on ? HIGH : LOW)
                                             : (on ? LOW  : HIGH)));
}

// Botões em modo toggle
bool updateToggle(uint8_t pin, int &lastRaw, unsigned long &lastMs, bool &state) {
  int raw = digitalRead(pin);
  unsigned long now = millis();
  if (raw != lastRaw) { lastMs = now; lastRaw = raw; }
  if ((now - lastMs) > DEBOUNCE_MS) {
    static int prevStable[3] = {HIGH, HIGH, HIGH};
    int idx = (pin == PIN_BTN_N ? 0 : pin == PIN_BTN_P ? 1 : 2);
    if (prevStable[idx] == HIGH && raw == LOW) { state = !state; }
    prevStable[idx] = raw;
  }
  return state;
}

// Lê o LDR e converte para pH (0–14)
float readPH() {
  uint32_t acc = 0;
  for (int i = 0; i < ADC_SAMPLES; i++) { acc += analogRead(PIN_LDR); delay(2); }
  float raw = acc / (float)ADC_SAMPLES;  // 0..4095
  return (raw / 4095.0f) * 14.0f;        // 0..14
}

String phDescription(float ph) {
  if (ph < 6.9f) return "Ácido";
  else if (ph > 7.1f) return "Alcalino";
  else return "Neutro";
}

// =======================
// Leitura via Serial: "chuva=true" ou "chuva=false"
// =======================
void handleSerialInput() {
  static String line;
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\r') continue;
    if (c == '\n') {
      line.trim();
      line.toLowerCase();

      if (line.startsWith("chuva=")) {
        String val = line.substring(6);
        val.trim();
        if (val == "true") {
          chuva = true;
        } else if (val == "false") {
          chuva = false;
        } else {
          Serial.println(F("Comando inválido. Use 'chuva=true' ou 'chuva=false'."));
        }
      }
      line = "";
    } else {
      if (line.length() < 64) line += c;
    }
  }
}

// =======================
// Setup
// =======================
void setup() {
  Serial.begin(115200);
  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_RELAY, OUTPUT);
  setRelay(false);

  analogReadResolution(12);
  analogSetPinAttenuation(PIN_LDR, ADC_11db);
  dht.begin();

  Serial.println(F("N P K | pH | Estado(pH) | Umid(%) | NPK_OK | Chuva | Bomba"));
  Serial.println(F("Digite 'chuva=true' ou 'chuva=false' no Serial Monitor."));
}

// =======================
// Loop
// =======================
void loop() {
  // 1) Ler possíveis comandos de chuva via Serial
  handleSerialInput();

  // 2) Atualiza botões (toggle)
  updateToggle(PIN_BTN_N, lastRawN, lastMsN, stateN);
  updateToggle(PIN_BTN_P, lastRawP, lastMsP, stateP);
  updateToggle(PIN_BTN_K, lastRawK, lastMsK, stateK);

  // 3) Leituras dos sensores
  float ph = readPH();
  float h  = dht.readHumidity();
  bool dht_ok = !isnan(h);

  const bool NPK_OK    = (stateN && stateP && stateK);
  const bool ph_neutro = (ph >= 6.9f && ph <= 7.1f);
  const bool humidity_low = dht_ok ? (h < HUMIDITY_MIN_IRRIGA) : false;

  // -------- Ir Além - Integração Python com API Pública (opcional 1)--------
  
  // Chuva == false → sem previsão de chuva
  
  bool liga = (NPK_OK && ph_neutro && humidity_low && !chuva);

  if (liga != bombaLigada) {
    setRelay(liga);
    bombaLigada = liga;
  }

  // 4) Saída serial
  Serial.print((int)stateN); Serial.print(' ');
  Serial.print((int)stateP); Serial.print(' ');
  Serial.print((int)stateK); Serial.print(" | ");
  Serial.print(ph, 2);       Serial.print(" | ");
  Serial.print(phDescription(ph)); Serial.print(" | ");
  if (dht_ok) Serial.print(h, 1); else Serial.print("NaN");
  Serial.print(" | ");
  Serial.print(NPK_OK ? "true" : "false"); Serial.print(" | ");
  Serial.print(chuva ? "true" : "false"); Serial.print(" | ");
  Serial.println(bombaLigada ? "ON" : "OFF");

  delay(250);
}
