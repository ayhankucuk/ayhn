// ! Bu araç @ayhankucuk tarafından | @Özel CloudStream Havuzu için yazılmıştır.

package com.ayhankucuk

import com.fasterxml.jackson.annotation.JsonProperty


data class AjaxSource(
    @JsonProperty("status")      val status: String,
    @JsonProperty("iframe")      val iframe: String,
    @JsonProperty("alternative") val alternative: String,
)