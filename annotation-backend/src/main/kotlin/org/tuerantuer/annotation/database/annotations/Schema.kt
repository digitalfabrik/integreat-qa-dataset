package org.tuerantuer.annotation.database.annotations

import kotlinx.datetime.Instant
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.javatime.CurrentTimestamp
import org.jetbrains.exposed.sql.javatime.timestamp
import org.jetbrains.exposed.sql.json.json
import org.tuerantuer.annotation.database.questions.Questions

object Annotations : IntIdTable() {
    val questionId = reference("questionId", Questions)
    val answerLines = varchar("answerLines", 50)
    val poorQuestion = bool("poorQuestion")
    val user = varchar("user", 64)
    val created = timestamp("created").defaultExpression(CurrentTimestamp())
}

class AnnotationEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<AnnotationEntity>(Annotations)

    var questionId by Annotations.questionId
    var answerLines by Annotations.answerLines
    var poorQuestion by Annotations.poorQuestion
    var user by Annotations.user
    var created by Annotations.created
}
