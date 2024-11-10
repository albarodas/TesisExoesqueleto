// Definición de pines para el primer motor (radial-ulnar)
#define MOTOR1_PWM 9
#define MOTOR1_IN1 4
#define MOTOR1_IN2 5

// Definición de pines para el segundo motor (flexión-extensión)
#define MOTOR2_PWM 10
#define MOTOR2_IN1 6
#define MOTOR2_IN2 7

// Parámetros de reducción de engranaje específicos para cada movimiento
const int gearReductionRadial = 4.2;
const int gearReductionUlnar = 5.0;
const int gearReductionFlexion = 1.0;
const int gearReductionExtension = 1.0;

// Velocidad del motor en grados por milisegundo (ajusta según las especificaciones del motor)
const float motorSpeedRadial = 1.0; // Ajusta la velocidad de giro del motor en grados por milisegundo
const float motorSpeedUlnar = 1.0;  // Ajusta la velocidad de giro del motor en grados por milisegundo
const float motorSpeedFlexion = 1.0; // Ajusta la velocidad de giro del motor en grados por milisegundo
const float motorSpeedExtension = 1.0; // Ajusta la velocidad de giro del motor en grados por milisegundo

// Variables para el tiempo de movimiento de cada motor
unsigned long moveDurationRadial = 0;
unsigned long moveDurationUlnar = 0;
unsigned long moveDurationFlexion = 0;
unsigned long moveDurationExtension = 0;

// Variables de tiempo de inicio para cada movimiento
unsigned long startTimeRadial = 0;
unsigned long startTimeUlnar = 0;
unsigned long startTimeFlexion = 0;
unsigned long startTimeExtension = 0;

// Flags de control para saber si los motores están en movimiento
bool motorRunningRadial = false;
bool motorRunningUlnar = false;
bool motorRunningFlexion = false;
bool motorRunningExtension = false;

bool emergencyStopActive = false;

// Variables de repeticiones
int repetitionsRadial = 1;
int repetitionsUlnar = 1;
int repetitionsFlexion = 1;
int repetitionsExtension = 1;
int currentRepetitionRadial = 0;
int currentRepetitionUlnar = 0;
int currentRepetitionFlexion = 0;
int currentRepetitionExtension = 0;

enum MotorState { STOPPED, MOVING_COUNTERCLOCKWISE, PAUSE_AFTER_COUNTERCLOCKWISE, MOVING_CLOCKWISE, PAUSE_AFTER_REPETITION };
MotorState motorRadialState = STOPPED;
MotorState motorUlnarState = STOPPED;
MotorState motorFlexionState = STOPPED;
MotorState motorExtensionState = STOPPED;

const unsigned long pauseDuration = 1000;

void setup() {
    Serial.begin(9600);

    // Configuración de pines del primer motor
    pinMode(MOTOR1_IN1, OUTPUT);
    pinMode(MOTOR1_IN2, OUTPUT);
    pinMode(MOTOR1_PWM, OUTPUT);

    // Configuración de pines del segundo motor
    pinMode(MOTOR2_IN1, OUTPUT);
    pinMode(MOTOR2_IN2, OUTPUT);
    pinMode(MOTOR2_PWM, OUTPUT);

    Serial.println("Sistema listo. Ingrese los comandos desde la interfaz.");
}

// Función para convertir ángulo a tiempo de giro del motor
unsigned long calculateMoveDuration(int angle, int gearReduction, float motorSpeed) {
    return (angle / motorSpeed) * gearReduction;
}

void loop() {
    if (emergencyStopActive) {
        stopMotor1();
        stopMotor2();
        motorRunningRadial = false;
        motorRunningUlnar = false;
        motorRunningFlexion = false;
        motorRunningExtension = false;
        emergencyStopActive = false;
        Serial.println("Paro de emergencia activado: Ambos motores detenidos.");
        return;
    }

    // Control del ciclo de movimientos para el primer motor (radial)
    if (motorRunningRadial && !motorRunningUlnar) {  // Solo corre si el motor ulnar no está activo
        switch (motorRadialState) {
            case MOVING_COUNTERCLOCKWISE:
                if (millis() - startTimeRadial >= moveDurationRadial) {
                    stopMotor1();
                    motorRadialState = PAUSE_AFTER_COUNTERCLOCKWISE;
                    startTimeRadial = millis();
                }
                break;

            case PAUSE_AFTER_COUNTERCLOCKWISE:
                if (millis() - startTimeRadial >= pauseDuration) {
                    moveMotor1Clockwise();
                    motorRadialState = MOVING_CLOCKWISE;
                    startTimeRadial = millis();
                }
                break;

            case MOVING_CLOCKWISE:
                if (millis() - startTimeRadial >= moveDurationRadial) {
                    stopMotor1();
                    motorRadialState = PAUSE_AFTER_REPETITION;
                    startTimeRadial = millis();
                }
                break;

            case PAUSE_AFTER_REPETITION:
                if (millis() - startTimeRadial >= pauseDuration) {
                    currentRepetitionRadial++;
                    if (currentRepetitionRadial < repetitionsRadial) {
                        moveMotor1CounterClockwise();
                        motorRadialState = MOVING_COUNTERCLOCKWISE;
                        startTimeRadial = millis();
                    } else {
                        motorRunningRadial = false;
                        motorRadialState = STOPPED;
                        Serial.println("Motor 1 (Radial) finalizó todas las repeticiones.");
                    }
                }
                break;

            default:
                break;
        }
    }

    // Control del ciclo de movimientos para el primer motor (ulnar)
    if (motorRunningUlnar && !motorRunningRadial) {  // Solo corre si el motor radial no está activo
        switch (motorUlnarState) {
            case MOVING_CLOCKWISE:
                if (millis() - startTimeUlnar >= moveDurationUlnar) {
                    stopMotor1();
                    motorUlnarState = PAUSE_AFTER_COUNTERCLOCKWISE;
                    startTimeUlnar = millis();
                }
                break;

            case PAUSE_AFTER_COUNTERCLOCKWISE:
                if (millis() - startTimeUlnar >= pauseDuration) {
                    moveMotor1CounterClockwise();
                    motorUlnarState = MOVING_COUNTERCLOCKWISE;
                    startTimeUlnar = millis();
                }
                break;

            case MOVING_COUNTERCLOCKWISE:
                if (millis() - startTimeUlnar >= moveDurationUlnar) {
                    stopMotor1();
                    motorUlnarState = PAUSE_AFTER_REPETITION;
                    startTimeUlnar = millis();
                }
                break;

            case PAUSE_AFTER_REPETITION:
                if (millis() - startTimeUlnar >= pauseDuration) {
                    currentRepetitionUlnar++;
                    if (currentRepetitionUlnar < repetitionsUlnar) {
                        moveMotor1Clockwise();
                        motorUlnarState = MOVING_CLOCKWISE;
                        startTimeUlnar = millis();
                    } else {
                        motorRunningUlnar = false;
                        motorUlnarState = STOPPED;
                        Serial.println("Motor 1 (Ulnar) finalizó todas las repeticiones.");
                    }
                }
                break;

            default:
                break;
        }
    }

    // Control del ciclo de movimientos para el segundo motor (flexión)
    if (motorRunningFlexion && !motorRunningExtension) {  // Solo corre si el motor extensión no está activo
        switch (motorFlexionState) {
            case MOVING_COUNTERCLOCKWISE:
                if (millis() - startTimeFlexion >= moveDurationFlexion) {
                    stopMotor2();
                    motorFlexionState = PAUSE_AFTER_COUNTERCLOCKWISE;
                    startTimeFlexion = millis();
                }
                break;

            case PAUSE_AFTER_COUNTERCLOCKWISE:
                if (millis() - startTimeFlexion >= pauseDuration) {
                    moveMotor2Clockwise();
                    motorFlexionState = MOVING_CLOCKWISE;
                    startTimeFlexion = millis();
                }
                break;

            case MOVING_CLOCKWISE:
                if (millis() - startTimeFlexion >= moveDurationFlexion) {
                    stopMotor2();
                    motorFlexionState = PAUSE_AFTER_REPETITION;
                    startTimeFlexion = millis();
                }
                break;

            case PAUSE_AFTER_REPETITION:
                if (millis() - startTimeFlexion >= pauseDuration) {
                    currentRepetitionFlexion++;
                    if (currentRepetitionFlexion < repetitionsFlexion) {
                        moveMotor2CounterClockwise();
                        motorFlexionState = MOVING_COUNTERCLOCKWISE;
                        startTimeFlexion = millis();
                    } else {
                        motorRunningFlexion = false;
                        motorFlexionState = STOPPED;
                        Serial.println("Motor 2 (Flexión) finalizó todas las repeticiones.");
                    }
                }
                break;

            default:
                break;
        }
    }

    // Control del ciclo de movimientos para el segundo motor (extensión)
    if (motorRunningExtension && !motorRunningFlexion) {  // Solo corre si el motor flexión no está activo
        switch (motorExtensionState) {
            case MOVING_CLOCKWISE:
                if (millis() - startTimeExtension >= moveDurationExtension) {
                    stopMotor2();
                    motorExtensionState = PAUSE_AFTER_COUNTERCLOCKWISE;
                    startTimeExtension = millis();
                }
                break;

            case PAUSE_AFTER_COUNTERCLOCKWISE:
                if (millis() - startTimeExtension >= pauseDuration) {
                    moveMotor2CounterClockwise();
                    motorExtensionState = MOVING_COUNTERCLOCKWISE;
                    startTimeExtension = millis();
                }
                break;

            case MOVING_COUNTERCLOCKWISE:
                if (millis() - startTimeExtension >= moveDurationExtension) {
                    stopMotor2();
                    motorExtensionState = PAUSE_AFTER_REPETITION;
                    startTimeExtension = millis();
                }
                break;

            case PAUSE_AFTER_REPETITION:
                if (millis() - startTimeExtension >= pauseDuration) {
                    currentRepetitionExtension++;
                    if (currentRepetitionExtension < repetitionsExtension) {
                        moveMotor2Clockwise();
                        motorExtensionState = MOVING_CLOCKWISE;
                        startTimeExtension = millis();
                    } else {
                        motorRunningExtension = false;
                        motorExtensionState = STOPPED;
                        Serial.println("Motor 2 (Extensión) finalizó todas las repeticiones.");
                    }
                }
                break;

            default:
                break;
        }
    }

    // Lectura de comandos del puerto serial
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        // Comandos de calibración manual para el primer motor (Radial-Ulnar)
        if (command == "h") {  // Sentido horario para motor 1
            moveMotor1Clockwise();
            Serial.println("Motor 1: Moviendo en sentido horario (Radial-Ulnar).");
        } else if (command == "a") {  // Sentido antihorario para motor 1
            moveMotor1CounterClockwise();
            Serial.println("Motor 1: Moviendo en sentido antihorario (Radial-Ulnar).");
        } else if (command == "p") {  // Pausar motor 1
            stopMotor1();
            Serial.println("Motor 1: Movimiento pausado (Radial-Ulnar).");
        } else if (command == "d") {  // Establecer posición 0 para motor 1
            stopMotor1();
            Serial.println("Motor 1: Posición establecida en 0° (Radial-Ulnar).");

        // Comandos de calibración manual para el segundo motor (Flexión-Extensión)
        } else if (command == "H") {  // Sentido horario para motor 2
            moveMotor2Clockwise();
            Serial.println("Motor 2: Moviendo en sentido horario (Flexión-Extensión).");
        } else if (command == "A") {  // Sentido antihorario para motor 2
            moveMotor2CounterClockwise();
            Serial.println("Motor 2: Moviendo en sentido antihorario (Flexión-Extensión).");
        } else if (command == "P") {  // Pausar motor 2
            stopMotor2();
            Serial.println("Motor 2: Movimiento pausado (Flexión-Extensión).");
        } else if (command == "D") {  // Establecer posición 0 para motor 2
            stopMotor2();
            Serial.println("Motor 2: Posición establecida en 0° (Flexión-Extensión).");

        // Comandos de movimiento estándar
        } else if (command == "E") {
            emergencyStopActive = true;
        } else if (command.startsWith("R1:") && !motorRunningFlexion && !motorRunningExtension) {
            int angleRadial = command.substring(3, command.indexOf(',')).toInt(); // Ángulo ingresado por el usuario
            repetitionsRadial = command.substring(command.indexOf(',') + 1).toInt();
            currentRepetitionRadial = 0;

            // Calcular la duración del movimiento en función del ángulo y la reducción de engranaje
            moveDurationRadial = calculateMoveDuration(angleRadial, gearReductionRadial, motorSpeedRadial);

            motorRadialState = MOVING_COUNTERCLOCKWISE;
            motorRunningRadial = true;
            startTimeRadial = millis();
            moveMotor1CounterClockwise();
            Serial.println("Movimiento radial en motor 1 iniciado.");
        }

        // Comandos de movimiento ulnar
        else if (command.startsWith("U1:") && !motorRunningFlexion && !motorRunningExtension) {
            int angleUlnar = command.substring(3, command.indexOf(',')).toInt(); // Ángulo ingresado por el usuario
            repetitionsUlnar = command.substring(command.indexOf(',') + 1).toInt();
            currentRepetitionUlnar = 0;

            // Calcular la duración del movimiento en función del ángulo y la reducción de engranaje
            moveDurationUlnar = calculateMoveDuration(angleUlnar, gearReductionUlnar, motorSpeedUlnar);

            motorUlnarState = MOVING_CLOCKWISE;
            motorRunningUlnar = true;
            startTimeUlnar = millis();
            moveMotor1Clockwise();
            Serial.println("Movimiento ulnar en motor 1 iniciado.");
        }

        // Comandos de movimiento flexión
        else if (command.startsWith("F2:") && !motorRunningRadial && !motorRunningUlnar && !motorRunningExtension) {
            int angleFlexion = command.substring(3, command.indexOf(',')).toInt(); // Ángulo ingresado por el usuario
            repetitionsFlexion = command.substring(command.indexOf(',') + 1).toInt();
            currentRepetitionFlexion = 0;

            // Calcular la duración del movimiento en función del ángulo y la reducción de engranaje
            moveDurationFlexion = calculateMoveDuration(angleFlexion, gearReductionFlexion, motorSpeedFlexion);

            motorFlexionState = MOVING_COUNTERCLOCKWISE;
            motorRunningFlexion = true;
            startTimeFlexion = millis();
            moveMotor2CounterClockwise();
            Serial.println("Movimiento de flexión en motor 2 iniciado.");
        }

        // Comandos de movimiento extensión
        else if (command.startsWith("E2:") && !motorRunningRadial && !motorRunningUlnar && !motorRunningFlexion) {
            int angleExtension = command.substring(3, command.indexOf(',')).toInt(); // Ángulo ingresado por el usuario
            repetitionsExtension = command.substring(command.indexOf(',') + 1).toInt();
            currentRepetitionExtension = 0;

            // Calcular la duración del movimiento en función del ángulo y la reducción de engranaje
            moveDurationExtension = calculateMoveDuration(angleExtension, gearReductionExtension, motorSpeedExtension);

            motorExtensionState = MOVING_CLOCKWISE;
            motorRunningExtension = true;
            startTimeExtension = millis();
            moveMotor2Clockwise();
            Serial.println("Movimiento de extensión en motor 2 iniciado.");
        }
    }
}

// Funciones para control de los motores
void moveMotor1Clockwise() {
    digitalWrite(MOTOR1_IN1, HIGH);
    digitalWrite(MOTOR1_IN2, LOW);
    analogWrite(MOTOR1_PWM, 100);
}

void moveMotor1CounterClockwise() {
    digitalWrite(MOTOR1_IN1, LOW);
    digitalWrite(MOTOR1_IN2, HIGH);
    analogWrite(MOTOR1_PWM, 100);
}

void stopMotor1() {
    digitalWrite(MOTOR1_IN1, LOW);
    digitalWrite(MOTOR1_IN2, LOW);
    analogWrite(MOTOR1_PWM, 0);
}

void moveMotor2Clockwise() {
    digitalWrite(MOTOR2_IN1, HIGH);
    digitalWrite(MOTOR2_IN2, LOW);
    analogWrite(MOTOR2_PWM, 80);
}

void moveMotor2CounterClockwise() {
    digitalWrite(MOTOR2_IN1, LOW);
    digitalWrite(MOTOR2_IN2, HIGH);
    analogWrite(MOTOR2_PWM, 80);
}

void stopMotor2() {
    digitalWrite(MOTOR2_IN1, LOW);
    digitalWrite(MOTOR2_IN2, LOW);
    analogWrite(MOTOR2_PWM, 0);
}
