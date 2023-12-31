package org.tuerantuer.question.database

import kotlinx.datetime.toJavaInstant
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.database.*
import org.tuerantuer.annotation.models.Question
import org.tuerantuer.annotation.models.Row
import org.tuerantuer.annotation.models.WithId
import org.tuerantuer.annotation.models.serializable

fun insertQuestion(rowId: Int, question: Question) = transaction {
    insertQuestion(QuestionEntity[rowId].id, question)
}

fun insertQuestion(rowId: EntityID<Int>, question: Question) = transaction {
    val questionEntity = QuestionEntity.new {
        this.rowId = rowId
        this.question = question.question
        answerLines = Json.encodeToString(question.answerLines)
        created = question.created.toJavaInstant()
    }

    question.annotations.forEach { insertAnnotation(questionEntity.id, it) }
}

fun getQuestion(user: String, city: String? = null, language: String? = null, evidence: Boolean? = null): WithId<Row>? =
    transaction {
        val query = ((Rows innerJoin Questions) leftJoin Annotations)
            .slice(Rows.columns + Questions.columns + Annotations.questionId.count())
            // TODO no questions which the user already annotated
            .select { (Annotations.user neq user) and (Questions.archived eq false) }
            .groupBy(Questions.id)
            .orderBy(Annotations.questionId.count() to SortOrder.ASC)

        city?.let { query.andWhere { Rows.city eq it } }
        language?.let { query.andWhere { Rows.language eq it } }
        evidence?.let { query.andWhere { Questions.answerLines eq "[]" } }

        val minimumAnnotations = query.minOfOrNull { it[Annotations.questionId.count()] } ?: 0

        query
            .filter { it[Annotations.questionId.count()] == minimumAnnotations }
            .map {
                val questionId = it[Questions.id].value
                val row = RowEntity.wrapRow(it).serializable(listOf(QuestionEntity.wrapRow(it).serializable()))
                WithId(questionId, row)
            }
            .randomOrNull()
    }

fun archiveQuestion(questionId: Int) = transaction {
    QuestionEntity.findById(questionId)?.archived = true
}

fun getQuestionsCount(): Int = transaction {
    QuestionEntity.count().toInt()
}
