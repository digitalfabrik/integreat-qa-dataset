package org.tuerantuer.annotation.models

import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.tuerantuer.annotation.database.AnnotationEntity

@Serializable
data class Annotation(
    val answerLines: List<Int>,
    val poor: Boolean,
    val noAnswer: Boolean,
    val comment: String,
    val user: String,
    val created: Instant = Clock.System.now(),
    val archived: Boolean = false
)

fun AnnotationEntity.serializable() = Annotation(
    answerLines = Json.decodeFromString(answerLines),
    poor = poor,
    noAnswer = noAnswer,
    comment = comment,
    user = user,
    created = Instant.fromEpochMilliseconds(created.toEpochMilli()),
    archived = archived
)
