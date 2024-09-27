package org.tuerantuer.annotation.models

import kotlinx.serialization.Serializable
import org.tuerantuer.annotation.database.*

@Serializable
data class Row(
    val pageId: Int,
    val pagePath: String,
    val city: String,
    val language: String,
    val context: String,
    val questions: List<Question>,
    val model: String
)

fun RowEntity.serializable(questions: List<Question>? = null, all: Boolean = false) = Row(
    pageId = pageId,
    pagePath = pagePath,
    city = city,
    language = language,
    context = context,
    model = model,
    questions = questions ?: QuestionEntity.find { Questions.rowId eq this@serializable.id }
        .map { it.serializable(all) }
        .filter { !it.archived }
)
