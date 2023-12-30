package org.tuerantuer.annotation.models

import kotlinx.datetime.Instant
import kotlinx.serialization.Serializable
import kotlin.Annotation

@Serializable
data class Row(
    val pageId: Int,
    val city: String,
    val language: String,
    val context: String,
    val questions: List<Question>
)
