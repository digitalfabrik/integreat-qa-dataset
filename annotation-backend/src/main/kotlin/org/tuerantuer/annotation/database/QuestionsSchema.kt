package org.tuerantuer.annotation.database

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.javatime.CurrentTimestamp
import org.jetbrains.exposed.sql.javatime.timestamp

object Questions : IntIdTable() {
    val rowId = reference("rowId", Rows)
    val question = varchar("question", 250)
    val answerLines = varchar("answerLines", 50)
    val created = timestamp("created").defaultExpression(CurrentTimestamp())
    val archived = bool("archived").default(false)
    val annotationCount = integer("annotationCount").default(0)
}

class QuestionEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<QuestionEntity>(Questions)

    var rowId by Questions.rowId
    var question by Questions.question
    var answerLines by Questions.answerLines
    var created by Questions.created
    var archived by Questions.archived
    var annotationCount by Questions.annotationCount
}
