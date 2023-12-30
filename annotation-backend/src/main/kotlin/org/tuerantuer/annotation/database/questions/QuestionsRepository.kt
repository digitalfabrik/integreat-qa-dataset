package org.tuerantuer.annotation.database.questions

import kotlinx.datetime.Instant
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.database.annotations.AnnotationEntity
import org.tuerantuer.annotation.database.annotations.Annotations
import org.tuerantuer.annotation.models.Question
import org.tuerantuer.annotation.models.Row
import org.tuerantuer.annotation.models.serializable

fun insertQuestions(rows: List<Row>) = transaction {
    rows.forEach {
        it.questions.forEachIndexed { index, item ->
            QuestionEntity.new {
                pageId = it.pageId
                questionIndex = index
                city = it.city
                language = it.language
                context = it.context
                question = item.question
                answerLines = Json.encodeToString(item.answerLines)
            }
        }
    }
}

fun getQuestion(city: String? = null, language: String? = null, evidence: Boolean? = null): Row? =
    transaction {
        val query = (Questions leftJoin Annotations)
            .slice(Questions.columns + Annotations.questionId.count())
            .selectAll()
            .groupBy(Questions.id)
            .orderBy(Annotations.questionId.count() to SortOrder.ASC)

        city?.let { query.andWhere { Questions.city eq it } }
        language?.let { query.andWhere { Questions.language eq it } }
        evidence?.let { query.andWhere { Questions.answerLines eq "[]" } }

        val minimumAnnotations = query.minOfOrNull { it[Annotations.questionId.count()] } ?: 0

        return@transaction query
            .filter { it[Annotations.questionId.count()] == minimumAnnotations }
            .map {
                Row(
                    pageId = it[Questions.pageId],
                    city = it[Questions.city],
                    language = it[Questions.language],
                    context = it[Questions.context],
                    questions = listOf(
                        Question(
                            question = it[Questions.question],
                            answerLines = Json.decodeFromString(it[Questions.answerLines]),
                        )
                    )
                )
            }
            .randomOrNull()
    }

fun getCities(): List<String> = transaction {
    return@transaction Questions.slice(Questions.city).selectAll().groupBy(Questions.city).map { it[Questions.city] }
}

fun getLanguages(): List<String> = transaction {
    return@transaction Questions.slice(Questions.language).selectAll().groupBy(Questions.language)
        .map { it[Questions.language] }
}

fun exportQuestions(): String {
    val rows = transaction {
        val questions = QuestionEntity.all().groupBy { it.pageId }
        questions.map {
            val first = it.value.first()
            Row(
                pageId = first.pageId,
                city = first.city,
                language = first.language,
                context = first.context,
                questions = it.value.map { question -> question.serializable() }
            )
        }
    }

    println("adsf")
    rows.forEach { println(Json.encodeToString(it)) }
    return ""
}
