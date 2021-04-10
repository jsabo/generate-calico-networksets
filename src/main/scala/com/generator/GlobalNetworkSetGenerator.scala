package com.generator
import java.io.PrintWriter
import play.api.libs.json._
import play.api.libs.functional.syntax._
import java.io.File
import com.typesafe.config.{ Config, ConfigFactory }

class GlobalNetworkSet(name: String, nets: List[String]) {
  private val netStringTemplate = "  - "
  override def toString: String = {
    val netsString = nets.map(s => netStringTemplate+s).mkString("\n")
    s"""apiVersion: projectcalico.org/v3
kind: GlobalNetworkSet
metadata:
  name: ${name.toLowerCase}
  labels:
    cloud-service: ${name.toLowerCase}
spec:
  nets:
$netsString
"""
  }
}

object GlobalNetworkSet {
  def apply(name: String, nets: List[String]): GlobalNetworkSet = new GlobalNetworkSet(name, nets)
}

object JsonHarvester {
  @throws(classOf[java.io.IOException])
  private def get(url: String): String = scala.io.Source.fromURL(url).mkString //todo need to check TLS cert

  def exportData[T](targetUrl: String)(implicit reads: Reads[T]): Seq[T] = {
    val allIpAddresses = get(targetUrl)
    (Json.parse(allIpAddresses) \ "prefixes").get.as[Seq[T]]
  }
}

object GlobalNetworkSetGenerator extends App {

  // todo same for azure

  val awsIpRanges = "https://ip-ranges.amazonaws.com/ip-ranges.json"

  case class Prefix(ipPrefix: String, region: String, service: String, networkBorderGroup: String)

  implicit val awsPrefixReads: Reads[Prefix] = (
    (JsPath \ "ip_prefix").read[String] and
      (JsPath \ "region").read[String] and
      (JsPath \ "service").read[String] and
      (JsPath \ "network_border_group").read[String]
    ) (Prefix.apply _)

  private def writeToFile(filename: String, contents: String): Unit = {
    new PrintWriter(filename) { write(contents); close }
  }

  val awsAddresses = JsonHarvester.exportData[Prefix](awsIpRanges)(awsPrefixReads)
  val services = awsAddresses.map(_.service).toSet.toList
  val serviceMap = services.map(s => s -> awsAddresses.filter(_.service == s).map(_.ipPrefix).toList).toMap
  val yamlList = serviceMap.map(s => GlobalNetworkSet(s._1.replace("_","-"), s._2).toString)

  // this can be set into the JVM environment variables, you can easily find it on google

  val configPath = scala.reflect.io.File(".").toAbsolute.toString() + "/conf/application.conf"
  val config = ConfigFactory.parseFile(new File(configPath))
  val outputPath = config.getString("calicofun.generator.outputpath")

  writeToFile(s"${outputPath}AwsGlobalNetworkSet.yaml", yamlList.mkString("---\n"))
}
