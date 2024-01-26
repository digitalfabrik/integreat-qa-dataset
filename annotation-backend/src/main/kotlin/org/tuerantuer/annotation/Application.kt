package org.tuerantuer.annotation

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.cors.routing.*
import org.tuerantuer.annotation.database.Database

fun start(dev: Boolean) {
    Database.setup()
    embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
        module(dev)
    }.start(wait = true)
}

fun Application.module(dev: Boolean) {
    if (dev) {
        install(CORS) {
            allowHeader(HttpHeaders.AccessControlAllowOrigin)
            allowHeader(HttpHeaders.ContentType)
            anyHost()
        }
    }
    configureRouting()
    configureSerialization()
}
