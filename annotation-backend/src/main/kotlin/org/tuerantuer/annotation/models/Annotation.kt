package org.tuerantuer.annotation.models

import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.tuerantuer.annotation.database.annotations.AnnotationEntity
import org.tuerantuer.annotation.database.questions.QuestionEntity

@Serializable
data class Annotation(
    val answerLines: List<Int>,
    val poorQuestion: Boolean,
)

fun AnnotationEntity.serializable() = Annotation(
    answerLines = Json.decodeFromString(answerLines),
    poorQuestion = poorQuestion,
)
