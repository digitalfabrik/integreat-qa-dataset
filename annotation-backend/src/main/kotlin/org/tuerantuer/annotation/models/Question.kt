package org.tuerantuer.annotation.models

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.database.annotations.AnnotationEntity
import org.tuerantuer.annotation.database.annotations.Annotations
import org.tuerantuer.annotation.database.questions.QuestionEntity

@Serializable
data class Question(
    val question: String,
    val answerLines: List<Int>,
    val annotations: List<Annotation> = emptyList(),
)

fun QuestionEntity.serializable() = Question(
    question = question,
    answerLines = Json.decodeFromString(answerLines),
    annotations = transaction {
        AnnotationEntity.find { Annotations.questionId eq this@serializable.id }.map { it.serializable() }
    }
)
