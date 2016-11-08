
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: KBParallelrunInputParams</p>
 * <pre>
 * Input parameters for run() method.
 * module_name - SDK module name (ie. ManyHellos, RNAseq),
 * method_name - method in SDK module (TopHatcall, Hiseqcall etc each will have own _prepare(),
 *     _runEach(), _collect() methods defined),
 * service_ver - optional version of SDK module (may be dev/beta/release, or symantic version
 *     or particular git commit hash), it's release by default,
 * is_local - optional flag defining way of scheduling sub-job, in case is_local=false sub-jobs
 *     are scheduled against remote execution engine, if is_local=true then sub_jobs are run as
 *     local functions through CALLBACK mechanism, default value is false,
 * global_input - input data which is supposed to be sent as a part to 
 *     <module_name>.<method_name>_prepare() method,
 * time_limit - time limit in seconds, equals to 5000 by default.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "module_name",
    "method_name",
    "service_ver",
    "is_local",
    "global_input",
    "time_limit"
})
public class KBParallelrunInputParams {

    @JsonProperty("module_name")
    private String moduleName;
    @JsonProperty("method_name")
    private String methodName;
    @JsonProperty("service_ver")
    private String serviceVer;
    @JsonProperty("is_local")
    private Long isLocal;
    @JsonProperty("global_input")
    private UObject globalInput;
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

    public KBParallelrunInputParams withModuleName(String moduleName) {
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

    public KBParallelrunInputParams withMethodName(String methodName) {
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

    public KBParallelrunInputParams withServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
        return this;
    }

    @JsonProperty("is_local")
    public Long getIsLocal() {
        return isLocal;
    }

    @JsonProperty("is_local")
    public void setIsLocal(Long isLocal) {
        this.isLocal = isLocal;
    }

    public KBParallelrunInputParams withIsLocal(Long isLocal) {
        this.isLocal = isLocal;
        return this;
    }

    @JsonProperty("global_input")
    public UObject getGlobalInput() {
        return globalInput;
    }

    @JsonProperty("global_input")
    public void setGlobalInput(UObject globalInput) {
        this.globalInput = globalInput;
    }

    public KBParallelrunInputParams withGlobalInput(UObject globalInput) {
        this.globalInput = globalInput;
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

    public KBParallelrunInputParams withTimeLimit(Long timeLimit) {
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
        return ((((((((((((((("KBParallelrunInputParams"+" [moduleName=")+ moduleName)+", methodName=")+ methodName)+", serviceVer=")+ serviceVer)+", isLocal=")+ isLocal)+", globalInput=")+ globalInput)+", timeLimit=")+ timeLimit)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
