package org.tuerantuer.annotation

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.cors.routing.*
import org.tuerantuer.annotation.database.Database

fun main() {
    Database.setup()
    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module).start(wait = true)
}

fun Application.module() {
    install(CORS) {
        // TODO Dev only
        anyHost()
    }
    configureRouting()
    configureSerialization()
}
