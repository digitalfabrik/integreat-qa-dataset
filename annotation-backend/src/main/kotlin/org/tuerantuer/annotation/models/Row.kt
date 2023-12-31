package org.tuerantuer.annotation.models

import kotlinx.serialization.Serializable
import org.tuerantuer.annotation.database.*

@Serializable
data class Row(
    val pageId: Int,
    val city: String,
    val language: String,
    val context: String,
    val questions: List<Question>
)

fun RowEntity.serializable(questions: List<Question>? = null) = Row(
    pageId = pageId,
    city = city,
    language = language,
    context = context,
    questions = questions ?: QuestionEntity.find { Questions.rowId eq this@serializable.id }.map { it.serializable() }
)
