package org.tuerantuer.annotation.database

import kotlinx.datetime.toJavaInstant
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.constants.MAX_ANNOTATIONS_PER_QUESTION
import org.tuerantuer.annotation.models.*

fun insertQuestion(rowId: Int, question: Question) = transaction {
    insertQuestion(QuestionEntity[rowId].id, question)
}

fun insertQuestion(rowId: EntityID<Int>, question: Question) = transaction {
    val questionEntity = QuestionEntity.new {
        this.rowId = rowId
        this.question = question.question
        answerLines = Json.encodeToString(emptyList<Int>())
        created = question.created.toJavaInstant()
    }

    question.annotations.forEach { insertAnnotation(questionEntity.id, it) }
}

fun getQuestions(user: String, city: String? = null, language: String? = null, evidence: Boolean? = null): Query =
    transaction {
        val query = ((Rows innerJoin Questions) leftJoin Annotations)
            .slice(Rows.columns + Questions.columns)
            .select {
                // Exclude questions the user already annotated
                notExists(Annotations.select { (Annotations.user eq user) and (Annotations.questionId eq Questions.id) }) and
                        (Questions.archived eq false) and
                        (Questions.annotationCount less MAX_ANNOTATIONS_PER_QUESTION)
            }
            .groupBy(Rows.id, Questions.id)

        city?.let { query.andWhere { Rows.city eq it } }
        language?.let { query.andWhere { Rows.language eq it } }
        evidence?.let { query.andWhere { Questions.answerLines eq "[]" } }

        return@transaction query
    }

fun getQuestion(user: String, city: String? = null, language: String? = null, evidence: Boolean? = null): WithId<Row>? =
    transaction {
        val query = getQuestions(user, city, language, evidence)

        val leastAnnotations = query.minOfOrNull { it[Questions.annotationCount] } ?: 0

        query
            // Questions which have the least amount of annotations first
            .filter { it[Questions.annotationCount] == leastAnnotations }
            .map {
                val questionId = it[Questions.id].value
                val row = RowEntity.wrapRow(it).serializable(listOf(QuestionEntity.wrapRow(it).serializable()))
                WithId(questionId, row)
            }
            .randomOrNull()
    }

fun getQuestionSelections(user: String): List<QuestionSelection> = transaction {
    val pairs = getQuestions(user)
        .filter { it[Questions.annotationCount] < MAX_ANNOTATIONS_PER_QUESTION }
        .map { Pair(it[Rows.city], it[Rows.language]) }

    pairs.toSet().map {
        QuestionSelection(
            it.first,
            it.second,
            pairs.count { acc -> it.first == acc.first && it.second == acc.second })
    }
}

fun archiveQuestion(questionId: Int) = transaction {
    QuestionEntity.findById(questionId)?.archived = true
}

fun getQuestionsCount(): Int = transaction {
    QuestionEntity.count().toInt()
}
