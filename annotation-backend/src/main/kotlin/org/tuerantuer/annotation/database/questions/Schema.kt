package org.tuerantuer.annotation.database.questions

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.javatime.CurrentTimestamp
import org.jetbrains.exposed.sql.javatime.timestamp

object Questions : IntIdTable() {
    val pageId = integer("pageId")
    val questionIndex = integer("questionIndex")
    val city = varchar("city", 25)
    val language = varchar("language", 5)
    val question = varchar("question", 50)
    val answerLines = varchar("answerLines", 50)
    val context = varchar("context", 2500)
    val created = timestamp("created").defaultExpression(CurrentTimestamp())
}

class QuestionEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<QuestionEntity>(Questions)

    var pageId by Questions.pageId
    var questionIndex by Questions.questionIndex
    var city by Questions.city
    var language by Questions.language
    var question by Questions.question
    var answerLines by Questions.answerLines
    var context by Questions.context
    var created by Questions.created
}
