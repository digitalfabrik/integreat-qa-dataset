package org.tuerantuer.annotation

import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import org.tuerantuer.annotation.database.Database
import org.tuerantuer.annotation.database.getRows

fun main() {
    Database.setup()
//    insertQuestions(emptyList())
//    insertAnnotations(emptyList())
    getRows()

    embeddedServer(Netty, port = 8080, host = "0.0.0.0", module = Application::module).start(wait = true)
}

fun Application.module() {
    configureRouting()
    configureSerialization()
}
