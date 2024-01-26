package org.tuerantuer.annotation

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.cors.routing.*
import kotlinx.serialization.json.Json
import org.tuerantuer.annotation.database.Database
import org.tuerantuer.annotation.database.insertRows
import org.tuerantuer.annotation.models.Row
import java.io.File

fun main() {
    Database.setup()
    File("src/main/resources/data").walkTopDown().forEach {
        if (it.extension == "json") {
            insertRows(Json.decodeFromString<List<Row>>(it.readText()))
        }
    }

    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module).start(wait = true)
}

fun Application.module() {
    install(CORS) {
        // TODO Dev only
        allowHeader(HttpHeaders.AccessControlAllowOrigin)
        allowHeader(HttpHeaders.ContentType)
        anyHost()
    }
    configureRouting()
    configureSerialization()
}
