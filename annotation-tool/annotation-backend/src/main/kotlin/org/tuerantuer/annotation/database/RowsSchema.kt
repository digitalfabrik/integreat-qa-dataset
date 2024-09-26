package org.tuerantuer.annotation.database

import org.jetbrains.exposed.dao.IntEntity
import org.jetbrains.exposed.dao.IntEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.IntIdTable

object Rows : IntIdTable() {
    val pageId = integer("pageId")
    val pagePath = varchar("pagePath", 200)
    val city = varchar("city", 25)
    val language = varchar("language", 5)
    val context = varchar("context", 8192)
    val model = varchar("model", 200)
}

class RowEntity(id: EntityID<Int>) : IntEntity(id) {
    companion object : IntEntityClass<RowEntity>(Rows)

    var pageId by Rows.pageId
    var pagePath by Rows.pagePath
    var city by Rows.city
    var language by Rows.language
    var context by Rows.context
    var model by Rows.model
}
