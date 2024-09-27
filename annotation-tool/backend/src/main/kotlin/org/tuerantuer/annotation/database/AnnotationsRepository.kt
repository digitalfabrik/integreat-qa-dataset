package org.tuerantuer.annotation.database

import kotlinx.datetime.toJavaInstant
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.deleteAll
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.models.Annotation

fun insertAnnotation(questionId: Int, annotation: Annotation) = transaction {
    insertAnnotation(QuestionEntity[questionId].id, annotation)
}

fun insertAnnotation(questionId: EntityID<Int>, annotation: Annotation) = transaction {
    // Every user should only be allowed to do one annotation per question
    // If a user does a second annotation for a question, it is to correct the previous one
    val previousAnnotations = AnnotationEntity.find {
        (Annotations.questionId eq questionId) and
                (Annotations.user eq annotation.user) and
                (Annotations.skipped eq false)
    }
    previousAnnotations.forEach { it.archived = true }
    if (previousAnnotations.count() == 0L && !annotation.skipped) {
        QuestionEntity[questionId].annotationCount += 1
    }

    AnnotationEntity.new {
        this.questionId = questionId
        answerLines = Json.encodeToString(annotation.answerLines)
        poor = annotation.poor
        skipped = annotation.skipped
        noAnswer = annotation.noAnswer
        comment = annotation.comment
        user = annotation.user
        created = annotation.created.toJavaInstant()
    }
}

fun getAnnotationsCount(): Int = transaction {
    return@transaction AnnotationEntity.find { (Annotations.archived eq false) and (Annotations.skipped eq false) }.count().toInt()
}

fun deleteAnnotations(user: String? = null) = transaction {
    if (user == null) {
        Annotations.deleteAll()
    } else {
        Annotations.deleteWhere { Annotations.user eq user }
    }
}
