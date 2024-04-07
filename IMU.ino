// Brian Lesko 
// IMU on the Arduino BLE Sense Rev2

#include "Arduino_BMI270_BMM150.h"
#include <Arduino_LPS22HB.h>
#include <math.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1); 
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println("in G (earth gravity).");

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");
  Serial.println("Gyroscope in degrees/second");
  
  Serial.print("Magnetometer sample rate = ");
  Serial.print(magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println("in uT (micro Tesla).");

  if (!BARO.begin()) {
    Serial.println("Failed to initialize pressure sensor!");
    while (1);
  }

float x, y, z;
float rx, ry, rz;
float mx, my, mz;
struct Vector3D {
    float x, y, z;
};
Vector3D crossProduct(const Vector3D& v1, const Vector3D& v2) {
    Vector3D result;
    result.x = v1.y * v2.z - v1.z * v2.y;
    result.y = v1.z * v2.x - v1.x * v2.z;
    result.z = v1.x * v2.y - v1.y * v2.x;
    return result;
}
float norm(float x, float y, float z) {
    return sqrt(x * x + y * y + z * z);
}

}

void loop() {
  unsigned long startTime = millis(); // Start time of the loop

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    float magn = norm(x,y,z);
    Vector3D acc = {x/magn, y/magn, z/magn};

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(rx,ry, rz);
    roll += rx * dt, pitch += ry * dt, yaw += rz * dt;
    //float magn = norm(rx,ry,rz);
    //Vector3D gyr = {rx/magn, ry/magn, rz/magn};

  if (magneticFieldAvailable()) {
    IMU.readMagneticField(mx, my, mz);
    float magn = norm(mx,my,mz);
    Vector3D mag = {mx/magn, my/magn, mz/magn};
  }

  float pressure = BARO.readPressure();
  float altitude = 44330 * ( 1 - pow(pressure/101.325, 1/5.255) );

  // North East and -Acceleration form the coordinate frame of the stationary IMU, uncalibrated
  Vector3D E = crossProduct(-acc, mag);
  Vector3D N = crossProduct(E, -acc);

  unsigned long endTime = millis(); // End time of the loop
  dt = endTime - startTime
}