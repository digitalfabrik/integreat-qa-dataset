
val ktorVersion: String by project
val kotlinVersion: String by project
val logbackVersion: String by project
val exposedVersion: String by project

plugins {
    kotlin("jvm") version "1.9.22"
    kotlin("plugin.serialization") version "1.9.22"
    id("io.ktor.plugin") version "2.3.7"
}

group = "org.tuerantuer.annotation"
version = "0.0.1"

application {
    mainClass.set("org.tuerantuer.annotation.EntryKt")
}

repositories {
    mavenCentral()
}

dependencies {
    // Backend
    implementation("io.ktor:ktor-server-core-jvm")
    implementation("io.ktor:ktor-server-netty-jvm")
    implementation("io.ktor:ktor-serialization-kotlinx-json-jvm")
    implementation("io.ktor:ktor-server-content-negotiation-jvm")
    implementation("io.ktor:ktor-server-cors")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.3.2")
    implementation("ch.qos.logback:logback-classic:$logbackVersion")

    // Database
    implementation("org.jetbrains.exposed:exposed-core:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-dao:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-jdbc:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-java-time:$exposedVersion")
    implementation("org.jetbrains.exposed:exposed-json:$exposedVersion")
    implementation("org.postgresql:postgresql:42.6.0")
    implementation("com.kohlschutter.junixsocket:junixsocket-core:2.7.0")
    implementation("com.kohlschutter.junixsocket:junixsocket-common:2.7.0")
    implementation("net.postgis:postgis-jdbc:2021.1.0")

    // Utils
    implementation("com.github.ajalt.clikt:clikt:4.2.2")
    implementation("io.github.cdimascio:dotenv-kotlin:6.4.1")
}
