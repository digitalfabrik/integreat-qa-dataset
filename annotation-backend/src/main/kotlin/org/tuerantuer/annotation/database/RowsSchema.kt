package org.tuerantuer.annotation.database

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable

object Rows : IntIdTable() {
    val pageId = integer("pageId")
    val city = varchar("city", 25)
    val language = varchar("language", 5)
    val context = varchar("context", 5000)
}

class RowEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<RowEntity>(Rows)

    var pageId by Rows.pageId
    var city by Rows.city
    var language by Rows.language
    var context by Rows.context
}
