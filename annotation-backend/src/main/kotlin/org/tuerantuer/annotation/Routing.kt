package org.tuerantuer.annotation

import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.tuerantuer.annotation.database.*
import org.tuerantuer.annotation.models.Row
import org.tuerantuer.annotation.models.WithId
import org.tuerantuer.annotation.database.archiveQuestion
import org.tuerantuer.annotation.database.getQuestion
import org.tuerantuer.annotation.database.getQuestionsCount
import org.tuerantuer.annotation.models.Annotation

fun Application.configureRouting() {
    routing {
        route("/rows") {
            get {
                call.respond(getRows())
            }

            post {
                val rows = call.receive<List<Row>>()
                insertRows(rows)
            }
        }

        route("/question") {
            get {
                val user = call.request.queryParameters["user"]
                    ?: return@get call.respondText("Missing user", status = HttpStatusCode.BadRequest)

                val city = call.request.queryParameters["city"]
                val language = call.request.queryParameters["language"]
                val evidence = call.request.queryParameters["evidence"]?.toBoolean()

                val question = getQuestion(user, city, language, evidence)
                    ?: return@get call.respondText("No questions found", status = HttpStatusCode.NotFound)

                call.respond(question)
            }

            delete("{id}") {
                archiveQuestion(call.parameters["id"]?.toInt()!!)
                call.respond(HttpStatusCode.OK)
            }

            route("/count") {
                get {
                    call.respond(getQuestionsCount())
                }
            }
        }

        route("/annotation") {
            post {
                val annotation = call.receive<WithId<Annotation>>()
                insertAnnotation(annotation.id, annotation.value)
                call.respond(HttpStatusCode.OK)
            }

            get("/count") {
                call.respond(getAnnotationsCount())
            }
        }

        get("/question-selections") {
            val user = call.request.queryParameters["user"]
                ?: return@get call.respondText("Missing user", status = HttpStatusCode.BadRequest)
            call.respond(getQuestionSelections(user))
        }

        get("/cities") {
            call.respond(getCities())
        }

        get("/languages") {
            call.respond(getLanguages())
        }
    }
}
