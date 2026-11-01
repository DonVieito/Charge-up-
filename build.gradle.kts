plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
 namespace = "com.chargeup.navigation"
 compileSdk = 35
 defaultConfig { applicationId = "com.chargeup.navigation"; minSdk = 26; targetSdk = 35; versionCode = 1; versionName = "3.0.0-alpha1" }
 compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
 kotlinOptions { jvmTarget = "17" }
}
dependencies { implementation("org.maplibre.gl:android-sdk:11.5.1") }
