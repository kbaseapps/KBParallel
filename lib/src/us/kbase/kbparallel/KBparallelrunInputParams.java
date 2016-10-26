
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: KBparallelrunInputParams</p>
 * <pre>
 * run() method
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "module_name",
    "method_name",
    "service_ver",
    "method_params",
    "client_class_name",
    "time_limit"
})
public class KBparallelrunInputParams {

    @JsonProperty("module_name")
    private String moduleName;
    @JsonProperty("method_name")
    private String methodName;
    @JsonProperty("service_ver")
    private String serviceVer;
    @JsonProperty("method_params")
    private List<UObject> methodParams;
    @JsonProperty("client_class_name")
    private String clientClassName;
    @JsonProperty("time_limit")
    private Long timeLimit;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("module_name")
    public String getModuleName() {
        return moduleName;
    }

    @JsonProperty("module_name")
    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public KBparallelrunInputParams withModuleName(String moduleName) {
        this.moduleName = moduleName;
        return this;
    }

    @JsonProperty("method_name")
    public String getMethodName() {
        return methodName;
    }

    @JsonProperty("method_name")
    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public KBparallelrunInputParams withMethodName(String methodName) {
        this.methodName = methodName;
        return this;
    }

    @JsonProperty("service_ver")
    public String getServiceVer() {
        return serviceVer;
    }

    @JsonProperty("service_ver")
    public void setServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
    }

    public KBparallelrunInputParams withServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
        return this;
    }

    @JsonProperty("method_params")
    public List<UObject> getMethodParams() {
        return methodParams;
    }

    @JsonProperty("method_params")
    public void setMethodParams(List<UObject> methodParams) {
        this.methodParams = methodParams;
    }

    public KBparallelrunInputParams withMethodParams(List<UObject> methodParams) {
        this.methodParams = methodParams;
        return this;
    }

    @JsonProperty("client_class_name")
    public String getClientClassName() {
        return clientClassName;
    }

    @JsonProperty("client_class_name")
    public void setClientClassName(String clientClassName) {
        this.clientClassName = clientClassName;
    }

    public KBparallelrunInputParams withClientClassName(String clientClassName) {
        this.clientClassName = clientClassName;
        return this;
    }

    @JsonProperty("time_limit")
    public Long getTimeLimit() {
        return timeLimit;
    }

    @JsonProperty("time_limit")
    public void setTimeLimit(Long timeLimit) {
        this.timeLimit = timeLimit;
    }

    public KBparallelrunInputParams withTimeLimit(Long timeLimit) {
        this.timeLimit = timeLimit;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((("KBparallelrunInputParams"+" [moduleName=")+ moduleName)+", methodName=")+ methodName)+", serviceVer=")+ serviceVer)+", methodParams=")+ methodParams)+", clientClassName=")+ clientClassName)+", timeLimit=")+ timeLimit)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
