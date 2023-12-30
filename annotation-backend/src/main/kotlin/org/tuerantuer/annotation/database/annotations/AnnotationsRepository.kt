package org.tuerantuer.annotation.database.annotations

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.database.questions.QuestionEntity
import org.tuerantuer.annotation.models.Annotation

fun insertAnnotations(annotations: List<Annotation>) = transaction {
//    annotations.forEach {
//        AnnotationEntity.new {
//            questionId = QuestionEntity[it.questionId].id
//            answerLines = Json.encodeToString(it.answerLines)
//            poorQuestion = it.poorQuestion
//            user = it.user
//        }
//    }
}

fun getAnnotationsCount(): Int = transaction {
    return@transaction AnnotationEntity.count().toInt()
}
