import org.jetbrains.kotlin.gradle.dsl.KotlinJsCompile

plugins {
    kotlin("multiplatform") version "2.1.10"
}

repositories {
    mavenCentral()
}

kotlin {
    js {
        browser {}
        binaries.executable()
    }
}

tasks.withType<KotlinJsCompile>().configureEach {
    kotlinOptions {
        target = "es2015"
    }
}