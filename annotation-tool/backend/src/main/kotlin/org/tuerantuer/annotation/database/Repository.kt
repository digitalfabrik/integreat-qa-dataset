package org.tuerantuer.annotation.database

import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.tuerantuer.annotation.models.Row
import org.tuerantuer.annotation.models.serializable

fun insertRows(rows: List<Row>) = transaction {
    rows.forEach { row ->
        val previous =
            RowEntity.find { (Rows.model eq row.model) and (Rows.pageId eq row.pageId) and (Rows.city eq row.city) and (Rows.language eq row.language) }
        if (previous.empty()) {
            val rowEntity = RowEntity.new {
                pageId = row.pageId
                pagePath = row.pagePath
                city = row.city
                language = row.language
                context = row.context
                model = row.model
            }

            row.questions.forEach { insertQuestion(rowEntity.id, it) }
        }
    }
}

fun getRows(all: Boolean = false): List<Row> = transaction {
    RowEntity.all().map { it.serializable(all=all) }
}

fun getCities(): List<String> = transaction {
    Rows.slice(Rows.city).selectAll().groupBy(Rows.city).map { it[Rows.city] }
}

fun getLanguages(): List<String> = transaction {
    Rows.slice(Rows.language).selectAll().groupBy(Rows.language).map { it[Rows.language] }
}

fun drop() = transaction {
    SchemaUtils.drop(Annotations, Questions, Rows)
}
