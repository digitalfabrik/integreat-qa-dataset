package org.tuerantuer.annotation.models

import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.tuerantuer.annotation.database.AnnotationEntity

@Serializable
data class Annotation(
    val id: Int? = null,
    val answerLines: List<Int>,
    val poor: Boolean,
    val noAnswer: Boolean,
    val skipped: Boolean,
    val comment: String,
    val user: String,
    val created: Instant = Clock.System.now(),
    val archived: Boolean = false
)

fun AnnotationEntity.serializable() = Annotation(
    id = id.value,
    answerLines = Json.decodeFromString(answerLines),
    poor = poor,
    skipped = skipped,
    noAnswer = noAnswer,
    comment = comment,
    user = user,
    created = Instant.fromEpochMilliseconds(created.toEpochMilli()),
    archived = archived
)
