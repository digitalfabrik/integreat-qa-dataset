package org.tuerantuer.annotation.database

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.javatime.CurrentTimestamp
import org.jetbrains.exposed.sql.javatime.timestamp

object Annotations : IntIdTable() {
    val questionId = reference("questionId", Questions)
    val answerLines = varchar("answerLines", 50)
    val poor = bool("poorQuestion")
    val noAnswer = bool("noAnswer")
    val comment = varchar("comment", 1000)
    val user = varchar("user", 64)
    val created = timestamp("created").defaultExpression(CurrentTimestamp())
    val archived = bool("archived").default(false)
}

class AnnotationEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<AnnotationEntity>(Annotations)

    var questionId by Annotations.questionId
    var answerLines by Annotations.answerLines
    var poor by Annotations.poor
    var noAnswer by Annotations.noAnswer
    var comment by Annotations.comment
    var user by Annotations.user
    var created by Annotations.created
    var archived by Annotations.archived
}
