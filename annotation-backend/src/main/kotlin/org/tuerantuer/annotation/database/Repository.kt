package org.tuerantuer.annotation.database

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.models.Row
import org.tuerantuer.annotation.models.serializable
import org.tuerantuer.question.database.insertQuestion

fun insertRows(rows: List<Row>) = transaction {
    rows.forEach { row ->
        val rowEntity = RowEntity.new {
            pageId = row.pageId
            city = row.city
            language = row.language
            context = row.context
        }

        row.questions.forEach { insertQuestion(rowEntity.id, it) }
    }
}

fun getRows(): String {
    val rows = transaction {
        RowEntity.all().map { it.serializable() }
    }

    return rows.joinToString("\n") { Json.encodeToString(it) }
}

fun getCities(): List<String> = transaction {
    Rows.slice(Rows.city).selectAll().groupBy(Rows.city).map { it[Rows.city] }
}

fun getLanguages(): List<String> = transaction {
    Rows.slice(Rows.language).selectAll().groupBy(Rows.language).map { it[Rows.language] }
}
