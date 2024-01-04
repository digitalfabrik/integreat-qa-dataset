package org.tuerantuer.annotation.models

import kotlinx.serialization.Serializable

@Serializable
data class QuestionSelection(val city: String, val language: String, val count: Int)