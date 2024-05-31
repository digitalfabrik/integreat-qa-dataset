package org.tuerantuer.annotation.models

import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.tuerantuer.annotation.database.AnnotationEntity
import org.tuerantuer.annotation.database.Annotations
import org.tuerantuer.annotation.database.QuestionEntity

@Serializable
data class Question(
    val id: Int? = null,
    val question: String,
    val answerLines: List<Int>,
    val annotations: List<Annotation> = emptyList(),
    val created: Instant = Clock.System.now(),
    val archived: Boolean = false
)

fun QuestionEntity.serializable(all: Boolean = false) = Question(
    id = id.value,
    question = question,
    answerLines = Json.decodeFromString(answerLines),
    annotations = AnnotationEntity.find { Annotations.questionId eq this@serializable.id }
        .map { it.serializable() }
        .filter { all || (!it.skipped && !it.archived) },
    created = Instant.fromEpochMilliseconds(created.toEpochMilli()),
    archived = false
)
