
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
 * method - optional method where _prepare(), _runEach() and _collect() suffixes are applied,
 * prepare_method - optional method (if defined overrides _prepare suffix rule),
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
    "method",
    "prepare_method",
    "is_local",
    "global_input",
    "time_limit"
})
public class KBParallelrunInputParams {

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
    @JsonProperty("method")
    private FullMethodQualifier method;
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
    @JsonProperty("prepare_method")
    private FullMethodQualifier prepareMethod;
    @JsonProperty("is_local")
    private Long isLocal;
    @JsonProperty("global_input")
    private UObject globalInput;
    @JsonProperty("time_limit")
    private Long timeLimit;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

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
    @JsonProperty("method")
    public FullMethodQualifier getMethod() {
        return method;
    }

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
    @JsonProperty("method")
    public void setMethod(FullMethodQualifier method) {
        this.method = method;
    }

    public KBParallelrunInputParams withMethod(FullMethodQualifier method) {
        this.method = method;
        return this;
    }

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
    @JsonProperty("prepare_method")
    public FullMethodQualifier getPrepareMethod() {
        return prepareMethod;
    }

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
    @JsonProperty("prepare_method")
    public void setPrepareMethod(FullMethodQualifier prepareMethod) {
        this.prepareMethod = prepareMethod;
    }

    public KBParallelrunInputParams withPrepareMethod(FullMethodQualifier prepareMethod) {
        this.prepareMethod = prepareMethod;
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
        return ((((((((((((("KBParallelrunInputParams"+" [method=")+ method)+", prepareMethod=")+ prepareMethod)+", isLocal=")+ isLocal)+", globalInput=")+ globalInput)+", timeLimit=")+ timeLimit)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
