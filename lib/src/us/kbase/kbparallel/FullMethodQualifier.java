
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FullMethodQualifier</p>
 * <pre>
 * module_name - SDK module name (ie. ManyHellos, RNAseq),
 * method_name - method in SDK module (TopHatcall, Hiseqcall etc each will have own _prepare(),
 *     _runEach(), _collect() methods defined),
 * service_ver - optional version of SDK module (may be dev/beta/release, or symantic version
 *     or particular git commit hash), it's release by default,
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "module_name",
    "method_name",
    "service_ver"
})
public class FullMethodQualifier {

    @JsonProperty("module_name")
    private String moduleName;
    @JsonProperty("method_name")
    private String methodName;
    @JsonProperty("service_ver")
    private String serviceVer;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("module_name")
    public String getModuleName() {
        return moduleName;
    }

    @JsonProperty("module_name")
    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public FullMethodQualifier withModuleName(String moduleName) {
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

    public FullMethodQualifier withMethodName(String methodName) {
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

    public FullMethodQualifier withServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
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
        return ((((((((("FullMethodQualifier"+" [moduleName=")+ moduleName)+", methodName=")+ methodName)+", serviceVer=")+ serviceVer)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
